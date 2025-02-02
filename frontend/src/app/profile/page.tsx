"use client";

import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Coins, User } from 'lucide-react';
import { logger } from '@/lib/logger';

/**
 * Profile page showing user information and credit balance.
 * Will integrate with backend /user endpoint later.
 */
export default function ProfilePage() {
  const [userId, setUserId] = useState<string>('');
  const [userName, setUserName] = useState<string>('');
  const [isCreatingUser, setIsCreatingUser] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Load user ID from local storage on mount
  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    const storedUserName = localStorage.getItem('userName');
    if (storedUserId) setUserId(storedUserId);
    if (storedUserName) setUserName(storedUserName);
  }, []);

  const handleSetupUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    
    if (!userName.trim()) {
      setError('Please enter a username');
      return;
    }
    
    setIsCreatingUser(true);
    
    try {
      // Create form data
      const formData = new FormData();
      formData.append('telegram_id', `temp_${Date.now()}`);
      formData.append('username', userName);
      
      // Call backend to create user
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      logger.info('User creation response:', { data });
      
      if (!response.ok) {
        throw new Error(data.error || data.detail || 'Failed to create user profile');
      }
      
      // Save user info to local storage
      localStorage.setItem('userId', data.id);
      localStorage.setItem('userName', userName);
      
      setUserId(data.id);
      setSuccess('User profile created successfully!');
      
    } catch (error) {
      logger.error('Error creating user', { error });
      setError(error instanceof Error ? error.message : 'Failed to create user profile. Please try again.');
    } finally {
      setIsCreatingUser(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('userId');
    localStorage.removeItem('userName');
    setUserId('');
    setUserName('');
    setSuccess('Logged out successfully');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-2">Your Profile</h1>
        <p className="text-muted-foreground">Manage your account and credits</p>
      </div>

      {/* User Setup/Info Card */}
      <Card className="bg-gradient-to-r from-purple-50 to-pink-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="w-5 h-5" />
            {userId ? 'Your Profile' : 'Create Profile'}
          </CardTitle>
          <CardDescription>
            {userId ? 'Your account information' : 'Set up your temporary profile'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {userId ? (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">User ID</span>
                <span className="font-medium">{userId}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Username</span>
                <span className="font-medium">{userName}</span>
              </div>
              <Button 
                variant="destructive" 
                className="w-full"
                onClick={handleLogout}
              >
                Logout
              </Button>
            </div>
          ) : (
            <form onSubmit={handleSetupUser} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="username" className="text-sm text-muted-foreground">
                  Choose a Username
                </label>
                <Input
                  id="username"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  placeholder="Enter your username"
                  disabled={isCreatingUser}
                />
              </div>
              
              {error && (
                <div className="text-sm text-red-500 text-center p-3 bg-red-50 rounded-md">
                  {error}
                </div>
              )}
              
              {success && (
                <div className="text-sm text-green-500 text-center p-3 bg-green-50 rounded-md">
                  {success}
                </div>
              )}
              
              <Button
                type="submit"
                className="w-full"
                disabled={isCreatingUser}
              >
                {isCreatingUser ? 'Creating Profile...' : 'Create Profile'}
              </Button>
            </form>
          )}
        </CardContent>
      </Card>

      {/* Credits Card */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Coins className="w-5 h-5" />
            Credits Balance
          </CardTitle>
          <CardDescription>Available credits for AI interactions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <p className="text-4xl font-bold mb-4">0</p>
            <Button disabled={!userId}>
              Buy More Credits
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* User Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Your Activity</CardTitle>
          <CardDescription>Overview of your platform usage</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">AI Agents Created</span>
            <span className="font-medium">0</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">Total Chats</span>
            <span className="font-medium">0</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">Total Searches</span>
            <span className="font-medium">0</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 