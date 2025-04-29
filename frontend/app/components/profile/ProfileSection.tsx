import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "~/components/ui/card";
import { FiInfo } from "react-icons/fi";

interface ProfileSectionProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

export const ProfileSection: React.FC<ProfileSectionProps> = ({ title, description, children }) => (
  <Card className="mb-6">
    <CardHeader className="flex flex-row items-center gap-2">
      <FiInfo className="h-5 w-5 text-muted-foreground" />
      <div>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </div>
    </CardHeader>
    <CardContent>
      <dl className="divide-y divide-gray-200">{children}</dl>
    </CardContent>
  </Card>
);