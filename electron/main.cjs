const { app, BrowserWindow, screen, ipcMain } = require('electron')

function createWindow() {
  const windowSize = 132
  const margin = 20

  const win = new BrowserWindow({
    width: windowSize,
    height: windowSize,
    transparent: true,
    frame: false,
    resizable: false,
    webPreferences: {
      preload: require('path').join(__dirname, 'preload.cjs'),
    },
  })

  const { workArea } = screen.getPrimaryDisplay()

  win.setPosition(
    workArea.x + workArea.width - windowSize - margin,
    workArea.y + margin,
  )

  win.setAlwaysOnTop(true)

let dragging = false
let lastCursorX = 0
let lastCursorY = 0

ipcMain.on('buddy-start-drag', () => {
  const cursor = screen.getCursorScreenPoint()

  dragging = true
  lastCursorX = cursor.x
  lastCursorY = cursor.y
})

ipcMain.on('buddy-end-drag', () => {
  dragging = false
})

  ipcMain.on('buddy-set-ignore-mouse-events', (_event, ignore) => {
    win.setIgnoreMouseEvents(ignore, {
      forward: true,
    })
  })

setInterval(() => {
  if (win.isDestroyed()) {
    return
  }

  const cursor = screen.getCursorScreenPoint()

  if (dragging) {
    const deltaX = cursor.x - lastCursorX
    const deltaY = cursor.y - lastCursorY

    if (deltaX !== 0 || deltaY !== 0) {
      const [x, y] = win.getPosition()

      win.setPosition(
        x + deltaX,
        y + deltaY,
      )
    }

    lastCursorX = cursor.x
    lastCursorY = cursor.y
  }

  win.webContents.send(
    'buddy-cursor-position',
    cursor.x,
    cursor.y,
  )
}, 16)

  win.loadURL('http://localhost:5173')
}

app.whenReady().then(() => {
  createWindow()
})