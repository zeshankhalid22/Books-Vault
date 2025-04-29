import React from 'react';
import { cn } from "~/lib/utils";

interface ProfileFieldProps {
  label: string;
  value: string | number | React.ReactNode;
  alternating?: boolean;
}

export const ProfileField: React.FC<ProfileFieldProps> = ({ label, value, alternating = true }) => (
  <div className={cn(
    "px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6",
    alternating ? "bg-muted/50" : "bg-background"
  )}>
    <dt className="text-sm font-medium text-muted-foreground">{label}</dt>
    <dd className="mt-1 text-sm sm:col-span-2 sm:mt-0">{value}</dd>
  </div>
);