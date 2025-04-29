// zod validator adapter
import { z } from 'zod';

export const zodValidator = <T extends z.ZodTypeAny>(schema: T) => {
    return (values: unknown) => {
        const result = schema.safeParse(values);
        return result.success ? undefined : result.error.flatten().fieldErrors;
    };
};
