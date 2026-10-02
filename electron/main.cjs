const { app, BrowserWindow, screen } = require('electron')

function createWindow() {
  const windowSize = 132
  const margin = 20

  const win = new BrowserWindow({
    width: windowSize,
    height: windowSize,
    transparent: true,
    frame: false,
  })

  const { workArea } = screen.getPrimaryDisplay()

  win.setPosition(
    workArea.x + workArea.width - windowSize - margin,
    workArea.y + margin,
  )
  win.setAlwaysOnTop(true)

  win.loadURL('http://localhost:5173')
}

app.whenReady().then(() => {
  createWindow()
})