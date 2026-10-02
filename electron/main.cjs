const { app, BrowserWindow, screen } = require('electron')

function createWindow() {
  const windowSize = 627
  const margin = 5
  const zoom = 0.25

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

  win.webContents.setZoomFactor(zoom)

  win.loadURL('http://localhost:5173')
}

app.whenReady().then(() => {
  createWindow()
})