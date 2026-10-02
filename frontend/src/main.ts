import './style.css'
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