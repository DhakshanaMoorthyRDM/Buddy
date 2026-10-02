import { CHARACTER_ASSETS } from './character-layers'

export class CharacterRenderer {
  private container: HTMLElement
  private body: HTMLImageElement
  private head: HTMLImageElement
  private eyeOpen: HTMLImageElement
  private eyeClosed: HTMLImageElement
  private chest: HTMLImageElement

  constructor(container: HTMLElement) {
    this.container = container

    this.body = this.createLayer('character-body')
    this.head = this.createLayer('character-head')
    this.eyeOpen = this.createLayer('character-eye-open')
    this.eyeClosed = this.createLayer('character-eye-closed')
    this.chest = this.createLayer('character-chest')

    this.body.src = CHARACTER_ASSETS.body.body
    this.head.src = CHARACTER_ASSETS.head.head
    this.eyeOpen.src = CHARACTER_ASSETS.eye.openEye
    this.eyeClosed.src = CHARACTER_ASSETS.eye.closedEye
    this.chest.src = CHARACTER_ASSETS.chest.glow

    this.eyeOpen.style.opacity = '1'
    this.eyeClosed.style.opacity = '0'

    this.container.append(
      this.body,
      this.head,
      this.eyeOpen,
      this.eyeClosed,
      this.chest,
    )

    this.startBreathing()
    this.startChestPulse()
    this.startBlinking()
  }

  private startBreathing(): void {
    this.container.animate(
      [
        {
          transform: 'translateY(0px) scale(1)',
        },
        {
          transform: 'translateY(3px) scale(0.985)',
          offset: 0.45,
        },
        {
          transform: 'translateY(3px) scale(0.985)',
          offset: 0.55,
        },
        {
          transform: 'translateY(0px) scale(1)',
        },
      ],
      {
        duration: 3000,
        iterations: Infinity,
        easing: 'ease-in-out',
      },
    )
  }

  private startChestPulse(): void {
    this.chest.animate(
      [
        { opacity: 0.4 },
        { opacity: 1 },
        { opacity: 0.4 },
      ],
      {
        duration: 3000,
        iterations: Infinity,
        easing: 'ease-in-out',
      },
    )
  }

  private blink(): void {
    this.eyeClosed.animate(
      [
        { opacity: 0 },
        { opacity: 1 },
      ],
      {
        duration: 70,
        fill: 'forwards',
        easing: 'ease-in',
      },
    )

    this.eyeOpen.animate(
      [
        { opacity: 1 },
        { opacity: 0 },
      ],
      {
        duration: 70,
        fill: 'forwards',
        easing: 'ease-in',
      },
    )

    setTimeout(() => {
      this.eyeClosed.animate(
        [
          { opacity: 1 },
          { opacity: 0 },
        ],
        {
          duration: 90,
          fill: 'forwards',
          easing: 'ease-out',
        },
      )

      this.eyeOpen.animate(
        [
          { opacity: 0 },
          { opacity: 1 },
        ],
        {
          duration: 90,
          fill: 'forwards',
          easing: 'ease-out',
        },
      )
    }, 100)
  }

  private startBlinking(): void {
    const blinkLoop = () => {
      const delay = 3000 + Math.random() * 3000

      setTimeout(() => {
        this.blink()
        blinkLoop()
      }, delay)
    }

    blinkLoop()
  }

  private createLayer(className: string): HTMLImageElement {
    const image = document.createElement('img')

    image.className = className
    image.draggable = false
    image.alt = ''

    return image
  }
}