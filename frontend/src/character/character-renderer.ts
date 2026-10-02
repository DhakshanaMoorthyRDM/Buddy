import { CHARACTER_ASSETS } from './character-layers'

type CharacterState = 'awake' | 'sleeping' | 'waking'

export class CharacterRenderer {
  private container: HTMLElement
  private body: HTMLImageElement
  private head: HTMLImageElement
  private eyeOpen: HTMLImageElement
  private eyeClosed: HTMLImageElement
  private chest: HTMLImageElement

  private state: CharacterState = 'awake'

  private breathingAnimation?: Animation
  private chestAnimation?: Animation

  private blinkTimer?: ReturnType<typeof setTimeout>
  private sleepTimer?: ReturnType<typeof setTimeout>
  private wakeTimer?: ReturnType<typeof setTimeout>
  private sleepingBounce?: Animation

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

    this.container.addEventListener('mousedown', () => {
      if (this.state === 'awake') {
        this.pauseSleepTimer()
      }
    })

    window.addEventListener('mouseup', () => {
      if (this.state === 'awake') {
        this.startSleepTimer()
      }
    })

    this.startBreathing()
    this.startChestPulse()
    this.startBlinking()
    this.startSleepTimer()

    this.container.addEventListener('dblclick', () => {
      if (this.state === 'sleeping') {
        this.wake()
      }
    })
  }

  private startBreathing(): void {
    this.breathingAnimation = this.container.animate(
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
    this.chestAnimation = this.chest.animate(
      [
        { opacity: 1 },
        { opacity: 0 },
        { opacity: 1 },
      ],
      {
        duration: 3000,
        iterations: Infinity,
        easing: 'ease-in-out',
      },
    )
  }

  private blink(): void {
    if (this.state !== 'awake') {
      return
    }

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
      if (this.state !== 'awake') {
        return
      }

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
      if (this.state !== 'awake') {
        return
      }

      const delay = 3000 + Math.random() * 3000

      this.blinkTimer = setTimeout(() => {
        this.blink()
        blinkLoop()
      }, delay)
    }

    blinkLoop()
  }
  private pauseSleepTimer(): void {
    if (this.sleepTimer) {
      clearTimeout(this.sleepTimer)
      this.sleepTimer = undefined
    }
  }

  private startSleepTimer(): void {
    this.pauseSleepTimer()

    this.sleepTimer = setTimeout(() => {
      this.sleep()
    }, 30000)
  }

  private sleep(): void {
    if (this.state !== 'awake') {
      return
    }

    this.state = 'sleeping'

    if (this.blinkTimer) {
      clearTimeout(this.blinkTimer)
    }

    this.breathingAnimation?.cancel()
    this.chestAnimation?.cancel()

    this.eyeOpen.animate(
      [
        { opacity: 1 },
        { opacity: 0 },
      ],
      {
        duration: 250,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.eyeClosed.animate(
      [
        { opacity: 0 },
        { opacity: 1 },
      ],
      {
        duration: 250,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    setTimeout(() => {
      if (this.state !== 'sleeping') {
        return
      }

      this.sleepingBounce = this.head.animate(
        [
          {
            transform: 'translate(1px, -110px) scale(0.78)',
          },
          {
            transform: 'translate(1px, -107px) scale(0.78)',
          },
          {
            transform: 'translate(1px, -110px) scale(0.78)',
          },
        ],
        {
          duration: 2800,
          iterations: Infinity,
          easing: 'ease-in-out',
        },
      )

      this.eyeClosed.animate(
        [
          {
            transform: 'translate(1px, -110px) scale(0.78)',
          },
          {
            transform: 'translate(1px, -107px) scale(0.78)',
          },
          {
            transform: 'translate(1px, -110px) scale(0.78)',
          },
        ],
        {
          duration: 2800,
          iterations: Infinity,
          easing: 'ease-in-out',
        },
      )
    }, 950)

    this.chest.animate(
      [
        { opacity: 1 },
        { opacity: 0 },
      ],
      {
        duration: 70,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.body.animate(
      [
        {
          transform: 'translateY(0px) scale(1)',
          opacity: 1,
        },
        {
          transform: 'translateY(-70px) scale(0.9)',
          opacity: 0,
        },
      ],
      {
        duration: 900,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.head.animate(
      [
        {
          transform: 'translate(1px, -141px) scale(0.69)',
        },
        {
          transform: 'translate(1px, -110px) scale(0.78)',
        },
      ],
      {
        duration: 900,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.eyeClosed.animate(
      [
        {
          transform: 'translate(1px, -141px) scale(0.69)',
        },
        {
          transform: 'translate(1px, -110px) scale(0.78)',
        },
      ],
      {
        duration: 900,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )
  }

  private wake(): void {
    if (this.state !== 'sleeping') {
      return
    }

    this.state = 'waking'
    this.sleepingBounce?.cancel()

    this.blinkTwice()

    this.body.animate(
      [
        {
          transform: 'translateY(-70px) scale(0.9)',
          opacity: 0,
        },
        {
          transform: 'translateY(0px) scale(1)',
          opacity: 1,
        },
      ],
      {
        duration: 900,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.head.animate(
      [
        {
          transform: 'translate(1px, -110px) scale(0.78)',
        },
        {
          transform: 'translate(1px, -141px) scale(0.69)',
        },
      ],
      {
        duration: 900,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.eyeClosed.animate(
      [
        {
          transform: 'translate(1px, -110px) scale(0.78)',
        },
        {
          transform: 'translate(1px, -141px) scale(0.69)',
        },
      ],
      {
        duration: 900,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

    this.chest.animate(
      [
        { opacity: 0 },
        { opacity: 1 },
      ],
      {
        duration: 7000,
        fill: 'forwards',
        easing: 'ease-in-out',
      },
    )

this.wakeTimer = setTimeout(() => {
  this.state = 'awake'

  this.eyeClosed.getAnimations().forEach((animation) => {
    animation.cancel()
  })

  this.eyeOpen.getAnimations().forEach((animation) => {
    animation.cancel()
  })

  this.eyeClosed.style.opacity = '0'
  this.eyeOpen.style.opacity = '1'

  this.startBreathing()
  this.startChestPulse()
  this.startBlinking()
  this.startSleepTimer()
}, 950)
  }

  private blinkTwice(): void {
    const firstBlink = () => {
      this.eyeClosed.animate(
        [
          { opacity: 1 },
          { opacity: 0 },
        ],
        {
          duration: 100,
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
          duration: 100,
          fill: 'forwards',
          easing: 'ease-out',
        },
      )

      setTimeout(() => {
        this.eyeClosed.animate(
          [
            { opacity: 0 },
            { opacity: 1 },
          ],
          {
            duration: 100,
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
            duration: 100,
            fill: 'forwards',
            easing: 'ease-in',
          },
        )
      }, 120)
    }

    firstBlink()

    setTimeout(() => {
      firstBlink()
    }, 300)
  }

  private createLayer(className: string): HTMLImageElement {
    const image = document.createElement('img')

    image.className = className
    image.draggable = false
    image.alt = ''

    return image
  }
}