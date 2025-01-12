interface ResultTabsProps {
  activeTab?: 'summary' | 'authors'
  onTabChange?: (tab: 'summary' | 'authors') => void
}

export default function ResultTabs({ activeTab = 'summary', onTabChange }: ResultTabsProps) {
  return (
    <div className="flex border-b">
      <button
        className={`flex items-center gap-2 px-4 py-2 border-b-2 transition-colors font-['Inter'] font-semibold ${
          activeTab === 'summary'
            ? 'border-[#0098EA] text-[#0098EA]'
            : 'border-transparent text-gray-500'
        }`}
        onClick={() => onTabChange?.('summary')}
      >
        <svg width="20" height="20" viewBox="0 0 166 166" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-current">
          <path fillRule="evenodd" clipRule="evenodd" d="M2.63434 76.6401C-0.878116 80.1526 -0.878115 85.8474 2.63435 89.3599L18.8231 105.549C22.3356 109.061 28.0304 109.061 31.5429 105.549L33.4701 103.621C41.453 95.6385 54.3957 95.6385 62.3786 103.621C70.3615 111.604 70.3615 124.547 62.3786 132.53L60.4514 134.457C56.9389 137.97 56.9389 143.664 60.4514 147.177L76.6401 163.366C80.1526 166.878 85.8474 166.878 89.3599 163.366L163.366 89.3599C166.878 85.8474 166.878 80.1526 163.366 76.6401L147.177 60.4514C143.664 56.9389 137.97 56.9389 134.457 60.4514L134.216 60.6923C126.233 68.6751 113.291 68.6751 105.308 60.6923C97.3249 52.7094 97.3249 39.7666 105.308 31.7838L105.549 31.5429C109.061 28.0304 109.061 22.3356 105.549 18.8231L89.3599 2.63435C85.8474 -0.878113 80.1526 -0.878118 76.6401 2.63435L2.63434 76.6401ZM73.0524 71.8966C67.2394 77.7096 67.2394 87.1343 73.0524 92.9473C78.8654 98.7603 88.2901 98.7603 94.1031 92.9473C99.9161 87.1343 99.9161 77.7096 94.1031 71.8966C88.2901 66.0836 78.8654 66.0836 73.0524 71.8966Z" fill="currentColor"/>
        </svg>
        Summary
      </button>
      <button
        className={`flex items-center gap-2 px-4 py-2 border-b-2 transition-colors font-['Inter'] font-semibold ${
          activeTab === 'authors'
            ? 'border-[#0098EA] text-[#0098EA]'
            : 'border-transparent text-gray-500'
        }`}
        onClick={() => onTabChange?.('authors')}
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-5 h-5"
        >
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        By author
      </button>
    </div>
  )
}

