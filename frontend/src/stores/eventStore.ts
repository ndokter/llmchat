import { defineStore } from 'pinia'

export type EventHandler = (event: MessageEvent) => void

export const useEventStore = defineStore('event', {
    state: () => ({
        source: null as EventSource | null,
        subscribers: new Set<EventHandler>()
    }),

  actions: {
    connect() {
        if (this.source) return

        this.source = new EventSource(`${import.meta.env.VITE_API_URL}/event-stream`)

        this.source.onmessage = (event: MessageEvent) => {
            let eventData: MessageEvent
            try {
                eventData = JSON.parse(event.data)
            } catch {
                console.error('Error reading event-stream: ' + event.data)
                return
            }   
            this.subscribers.forEach((fn) => fn(eventData))
        }
    },

    subscribe(callback: (event: MessageEvent) => void) {
        if (!this.source)
            this.connect()

        this.subscribers.add(callback)

        // Returns unsubscribe method
        return () => this.subscribers.delete(callback)
    }
  },
})