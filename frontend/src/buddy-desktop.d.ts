interface Window {
  buddyDesktop: {
    startDrag: () => void
    endDrag: () => void
    setIgnoreMouseEvents: (ignore: boolean) => void
    onCursorPosition: (
      callback: (x: number, y: number) => void
    ) => void
  }
}