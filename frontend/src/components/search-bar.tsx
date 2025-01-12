import { Search } from 'lucide-react'

export default function SearchBar() {
  return (
    <div className="relative mb-4">
      <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
        <Search className="h-5 w-5 text-gray-400" />
      </div>
      <input
        type="text"
        placeholder="Search creators or topics"
        className="w-full bg-gray-100 text-black placeholder-gray-400 pl-10 pr-4 py-3 rounded-full focus:outline-none focus:ring-2 focus:ring-[#0098EA]"
      />
    </div>
  )
}

