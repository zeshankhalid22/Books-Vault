import React from 'react'
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";

import {useAuth} from "~/hooks/useAuth";
import {loginSchema} from "~/types/schema/loginSchema";
import type {loginFormData} from "~/types/formData/loginFormData";
import {Form} from "~/components/ui/form"
import FormField from "~/components/FormField";

const Login: React.FC = () => {
    const {login, isLoading, error} = useAuth();


    const form = useForm<loginFormData>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = (data: loginFormData) => {
        login(data.email, data.password);
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                    <FormField
                        label="Email"
                        name="email"
                        type="email"
                        register={form.register}
                        error={form.formState.errors.email}
                        placeholder="Enter your email"
                    />

                    <FormField
                        label="Password"
                        name="password"
                        type="password"
                        register={form.register}
                        error={form.formState.errors.password}
                        placeholder="Enter your password"
                    />

                    {error && (
                        <div className="text-red-500 text-sm">{error}</div>
                    )}

                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <input
                                id="remember-me"
                                name="remember-me"
                                type="checkbox"
                                className="h-4 w-4 text-blue-600 border-gray-300 rounded"
                            />
                            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                                Remember me
                            </label>
                        </div>

                        <div className="text-sm">
                            <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
                                Forgot your password?
                            </a>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                    >
                        {isLoading ? 'Signing in...' : 'Sign in'}
                    </button>
                </form>
            </Form>
        </div>
    );
};

export default Login;