const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('buddyDesktop', {

  startDrag: () => ipcRenderer.send('buddy-start-drag'),
  endDrag: () => ipcRenderer.send('buddy-end-drag'),

  setIgnoreMouseEvents: (ignore) =>
    ipcRenderer.send('buddy-set-ignore-mouse-events', ignore),

  onCursorPosition: (callback) => {
    ipcRenderer.on(
      'buddy-cursor-position',
      (_event, x, y) => {
        callback(x, y)
      },
    )
  },

})