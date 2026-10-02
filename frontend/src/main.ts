import './style.css'
import { CharacterRenderer } from './character/character-renderer'

const app = document.querySelector<HTMLDivElement>('#app')

if (!app) {
  throw new Error('App container not found')
}

const character = document.createElement('div')
character.className = 'character'

app.appendChild(character)

new CharacterRenderer(character)