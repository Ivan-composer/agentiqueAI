"use client";

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Coins } from 'lucide-react';

/**
 * Profile page showing user information and credit balance.
 * Will integrate with backend /user endpoint later.
 */
export default function ProfilePage() {
  // TODO: Replace with real API call
  const mockUser = {
    name: "John Doe",
    email: "john@example.com",
    credits: 10,
    agentsCreated: 2,
    totalChats: 15,
    totalSearches: 8
  };

  const handleBuyCredits = () => {
    // TODO: Implement credit purchase flow
    console.log('Buy credits clicked');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-2">Your Profile</h1>
        <p className="text-muted-foreground">Manage your account and credits</p>
      </div>

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
            <p className="text-4xl font-bold mb-4">{mockUser.credits}</p>
            <Button onClick={handleBuyCredits}>
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
            <span className="font-medium">{mockUser.agentsCreated}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">Total Chats</span>
            <span className="font-medium">{mockUser.totalChats}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">Total Searches</span>
            <span className="font-medium">{mockUser.totalSearches}</span>
          </div>
        </CardContent>
      </Card>

      {/* User Info */}
      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
          <CardDescription>Your personal details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">Name</span>
            <span className="font-medium">{mockUser.name}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground">Email</span>
            <span className="font-medium">{mockUser.email}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 