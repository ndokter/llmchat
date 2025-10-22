import { defineStore } from "pinia";

export interface Model {
    id: Number
    name: string
    alias: string | null
    system_prompt: string | null
    provider_id: number
}
export interface NewModel {
    name: string
    alias: string
    system_prompt: string | null
    provider_id: number
}

export const useModelsStore = defineStore('models', {
    state: () => ({
        models: [] as Model[],
        loading: false,
        error: null
    }),

    actions: {
        async fetchModels() {
            this.loading = true
            this.error = null
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/models`)
                if (!res.ok) throw new Error('Failed to fetch models')
                const data = (await res.json()) as Model[]
                console.log('retrieved: ', this.models)
                this.models = data
            } catch (err: any) {
                this.error = err.message ?? 'Unknown error'
            } finally {
                this.loading = false
            }
        },

        async createModel(payload: NewModel): Promise<Model> {
            this.loading = true
            this.error = null

            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/models`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                })
                if (!res.ok) throw new Error('Failed to create model')
                const model = (await res.json()) as Model
                await this.fetchModels()
                return model
            } catch (err: any) {
                this.error = err.message ?? 'Unknown error'
                throw err
            } finally {
                this.loading = false
            }
        },

        async updateModel(id: number, payload: NewModel): Promise<void> {
            this.loading = true
            this.error = null
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/models/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                })
                if (!res.ok) throw new Error(`Failed to update model: ${res.status}`)
                await this.fetchModels()
            } catch (err: any) {
                console.error(err)
                this.error = err.message ?? 'Unknown error'
            } finally {
                this.loading = false
            }
        },

        async deleteModel(id: number): Promise<void> {
            this.loading = true
            this.error = null
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/models/${id}`, {
                    method: 'DELETE',
                })
                if (!res.ok) throw new Error(`Failed to delete model: ${res.status}`)
                await this.fetchModels()
            } catch (err: any) {
                console.error(err)
                this.error = err.message ?? 'Unknown error'
            } finally {
                this.loading = false
            }
        },
    }
})