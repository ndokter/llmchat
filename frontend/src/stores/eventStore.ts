import { defineStore } from 'pinia'


export interface EventData {
  type: string;
  body: any;
}

// interface ChatCompletionEvent extends EventData {
//   type: "chat:completion";
//   body: {
//     chat_id: number;
//     message_id: number;
//     status: string;
//     content: string;
//   };
// }

// interface ChatErrorEvent extends BaseEEventDatavent {
//   type: "chat:error";
//   body: {
//     chat_id: number;
//     error: string;
//   };
// }

export type EventHandler = (event: EventData) => void

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

            let eventData: EventData;
            try {
                eventData = JSON.parse(event.data)

            } catch {
                console.error('Error reading event-stream: ' + event.data)
                return
            }   
            this.subscribers.forEach((fn) => fn(eventData))

        }
    },

    subscribe(callback: EventHandler) {
        if (!this.source)
            this.connect()

        this.subscribers.add(callback)
    },

    unsubscribe(callback: EventHandler) {
        this.subscribers.delete(callback)
    }
  },
})