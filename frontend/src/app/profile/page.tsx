"use client";

import { CreditCard, History } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

/**
 * Profile page component showing user information and credits.
 * Will integrate with backend user endpoints later.
 */
export default function ProfilePage() {
  // TODO: Integrate with backend to get real user data
  const mockUser = {
    name: "@user_telegram_id",
    credits: 15,
    transactions: [
      { id: 1, type: 'initial', amount: 15, date: new Date().toISOString() }
    ]
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-2">Profile</h1>
        <p className="text-muted-foreground">{mockUser.name}</p>
      </div>

      {/* Credits Card */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-lg font-semibold">Credits Balance</CardTitle>
          <CreditCard className="text-primary w-6 h-6" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-primary">
            {mockUser.credits}
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Use credits to chat with AI agents
          </p>
        </CardContent>
      </Card>

      {/* Transaction History */}
      <Card>
        <CardHeader className="flex flex-row items-center space-y-0 pb-2">
          <History className="w-5 h-5 text-muted-foreground mr-2" />
          <CardTitle className="text-lg">Transaction History</CardTitle>
        </CardHeader>
        <CardContent className="divide-y">
          {mockUser.transactions.map(transaction => (
            <div key={transaction.id} className="py-4 first:pt-0 last:pb-0">
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">
                    {transaction.type === 'initial' ? 'Initial Credits' : transaction.type}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {new Date(transaction.date).toLocaleDateString()}
                  </p>
                </div>
                <div className="text-green-600 font-medium">
                  +{transaction.amount}
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
} 