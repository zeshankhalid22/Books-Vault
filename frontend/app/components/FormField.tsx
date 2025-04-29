import * as React from 'react';
import type { FieldError, UseFormRegister, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormItem, FormLabel, FormMessage } from "~/components/ui/form";
import { Input } from "~/components/ui/input";

export type FormFieldProps<T extends FieldValues> = {
  type: string;
  placeholder: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  valueAsNumber?: boolean;
  label?: string;
  className?: string;
};

const FormField = <T extends FieldValues>({
  type,
  placeholder,
  name,
  register,
  error,
  valueAsNumber,
  label,
  className = "",
}: FormFieldProps<T>) => (
  <FormItem className="form-field">
    {label && <FormLabel htmlFor={String(name)}>{label}</FormLabel>}
    <FormControl>
      <Input
        id={String(name)}
        type={type}
        placeholder={placeholder}
        className={className}
        {...register(name, { valueAsNumber })}
      />
    </FormControl>
    {error && <FormMessage>{error.message}</FormMessage>}
  </FormItem>
);

export default FormField;