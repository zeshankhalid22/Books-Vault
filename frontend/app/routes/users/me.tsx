import { useEffect, useState } from "react";
import { FiKey, FiEdit, FiLoader } from "react-icons/fi";
import { Navigate } from "react-router";
import { Button } from "~/components/ui/button";
import { ProfileSection } from "~/components/profile/ProfileSection";
import { useAuth } from "~/hooks/useAuth";

const ProfileActions = () => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 mt-6">
      <Button variant="outline" className="flex items-center gap-2">
        <FiKey className="h-4 w-4"/>
        Change Password
      </Button>
      <Button className="flex items-center gap-2">
        <FiEdit className="h-4 w-4"/>
        Edit Profile
      </Button>
    </div>
  );
};

export default function ProfilePage() {
  const { user, isAuthenticated, isLoading, verifyAuth } = useAuth();
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const loadUserData = async () => {
      if (!user) {
        await verifyAuth();
      }
      setIsInitialized(true);
    };

    loadUserData();
  }, [verifyAuth, user]);

  // Handle loading state
  if (isLoading || !isInitialized) {
    return (
      <div className="flex justify-center items-center h-64">
        <FiLoader className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  // Handle not authenticated state - use Navigate component instead of loader
  if (!isAuthenticated || !user) {
    return <Navigate to="/users/auth" replace />;
  }

  return (
    <div className="container max-w-4xl py-8">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>

      <ProfileSection
        title="Personal Information"
        description="Manage your personal details">
        <div className="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Full name</dt>
          <dd className="mt-1 text-sm sm:col-span-2 sm:mt-0">{user.name}</dd>
        </div>
        <div className="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Email address</dt>
          <dd className="mt-1 text-sm sm:col-span-2 sm:mt-0">{user.email}</dd>
        </div>
        {user.role && (
          <div className="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
            <dt className="text-sm font-medium text-gray-500">Role</dt>
            <dd className="mt-1 text-sm sm:col-span-2 sm:mt-0">{user.role}</dd>
          </div>
        )}
      </ProfileSection>

      <ProfileActions />
    </div>
  );
}