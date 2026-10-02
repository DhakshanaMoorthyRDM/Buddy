import './style.css'
import { CHARACTER_ASSETS } from './character/character-layers'
import { CharacterRenderer } from './character/character-renderer'

const app = document.querySelector<HTMLDivElement>('#app')

if (!app) {
  throw new Error('App container not found')
}

const characterStage = document.createElement('div')
characterStage.className = 'character-stage'

const characterScale = document.createElement('div')
characterScale.className = 'character-scale'

const character = document.createElement('div')
character.className = 'character'

characterScale.appendChild(character)
characterStage.appendChild(characterScale)
app.appendChild(characterStage)

new CharacterRenderer(character)

const hitCanvas = document.createElement('canvas')
hitCanvas.width = 627
hitCanvas.height = 627

const hitContext = hitCanvas.getContext('2d', {
  willReadFrequently: true,
})

if (!hitContext) {
  throw new Error('Could not create hit-test canvas')
}

const bodyImage = new Image()
const headImage = new Image()

bodyImage.src = CHARACTER_ASSETS.body.body
headImage.src = CHARACTER_ASSETS.head.head

let imagesLoaded = 0

const prepareHitTest = () => {
  imagesLoaded++

  if (imagesLoaded < 2) {
    return
  }

  hitContext.clearRect(0, 0, 627, 627)

  hitContext.drawImage(
    bodyImage,
    0,
    0,
    627,
    627,
  )

  hitContext.save()

hitContext.translate(1, -141)
hitContext.translate(313.5, 313.5)
hitContext.scale(0.69, 0.69)
hitContext.translate(-313.5, -313.5)

hitContext.drawImage(
  headImage,
  0,
  0,
  627,
  627,
)

hitContext.restore()
}

bodyImage.onload = prepareHitTest
headImage.onload = prepareHitTest

let dragging = false

window.buddyDesktop.onCursorPosition((cursorX, cursorY) => {
  if (imagesLoaded < 2) {
    return
  }

  const rect = characterStage.getBoundingClientRect()

  const x = Math.floor(
    (cursorX - rect.left - window.screenX) / rect.width * 627,
  )

  const y = Math.floor(
    (cursorY - rect.top - window.screenY) / rect.height * 627,
  )

  if (
    x < 0 ||
    x >= 627 ||
    y < 0 ||
    y >= 627
  ) {
    window.buddyDesktop.setIgnoreMouseEvents(true)
    return
  }

  const alpha = hitContext.getImageData(x, y, 1, 1).data[3]

  if (alpha === 0) {
    window.buddyDesktop.setIgnoreMouseEvents(true)
  } else {
    window.buddyDesktop.setIgnoreMouseEvents(false)
  }
})

characterStage.addEventListener('mousedown', (event) => {
  if (event.button !== 0 || imagesLoaded < 2) {
    return
  }

  const rect = characterStage.getBoundingClientRect()

  const x = Math.floor(
    (event.clientX - rect.left) / rect.width * 627,
  )

  const y = Math.floor(
    (event.clientY - rect.top) / rect.height * 627,
  )

  if (
    x < 0 ||
    x >= 627 ||
    y < 0 ||
    y >= 627
  ) {
    return
  }

  const alpha = hitContext.getImageData(x, y, 1, 1).data[3]

  if (alpha === 0) {
    return
  }

  dragging = true

  window.buddyDesktop.startDrag()
})


window.addEventListener('mouseup', () => {
  if (!dragging) {
    return
  }

  dragging = false
  window.buddyDesktop.endDrag()
})
