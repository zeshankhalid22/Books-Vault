'use client'

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'

import { registerSchema } from '~/types/schema/registerSchema'
import FormField from '~/components/FormField'
import { Form } from '~/components/ui/form'

// 👇 Directly infer form data type from the schema
type RegisterFormData = z.infer<typeof registerSchema>

const Register: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false)
    const [apiError, setApiError] = useState<string | null>(null)

    const form= useForm<RegisterFormData>({
        defaultValues: {
            username: '',
            email: '',
            name: '',
            password: '',
        },
        resolver: zodResolver(registerSchema),
    })

    const onSubmit = async (data: RegisterFormData) => {
        setIsLoading(true)
        setApiError(null)

        try {
            const response = await axios.post('http://127.0.0.1:8000/users/', data, {
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            console.log('Registration successful:', response.data)
        } catch (error: any) {
            console.error('Registration error:', error)
            setApiError(error?.response?.data?.detail || 'Registration failed.')
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
            <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                <div className="space-y-4">
                    <h1 className="text-3xl font-bold text-center mb-6">Register</h1>

                    {apiError && (
                        <div className="p-3 bg-red-100 text-red-700 rounded-md mb-4">
                            {apiError}
                        </div>
                    )}

                    {/* 👇 Use FormField as a generic component */}
                    <FormField<RegisterFormData>
                        type="email"
                        placeholder="Email"
                        name="email"
                        label="Email Address"
                        register={form.register}
                        error={form.formState.errors.email}
                    />

                    <FormField<RegisterFormData>
                        type="text"
                        placeholder="Username"
                        name="username"
                        label="Username"
                        register={form.register}
                        error={form.formState.errors.username}
                    />

                    <FormField<RegisterFormData>
                        type="text"
                        placeholder="Name"
                        name="name"
                        label="Full Name"
                        register={form.register}
                        error={form.formState.errors.name}
                    />

                    <FormField<RegisterFormData>
                        type="password"
                        placeholder="****"
                        name="password"
                        label="Password"
                        register={form.register}
                        error={form.formState.errors.password}
                    />

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:bg-blue-400"
                    >
                        {isLoading ? 'Registering...' : 'Register'}
                    </button>
                </div>
            </form>
            </Form>
            </div>
    )
}

export default Register
