import SearchInput from '@/components/search-input'
import BottomNav from '@/components/bottom-nav'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-white via-[#E5F7FF]/20 to-white px-4">
      <div className="flex-1 w-full max-w-md flex flex-col items-center justify-center gap-8 -mt-20">
        <div className="text-center space-y-6">
          <div className="flex items-center justify-center gap-2">
            <h1 className="text-[28px] font-bold bg-gradient-to-r from-[#08C6C9] to-[#0098EA] bg-clip-text text-transparent font-[&apos;Inter&apos;]">
              AGENTIQUE
            </h1>
            <svg width="28" height="28" viewBox="0 0 45 44" fill="none" xmlns="http://www.w3.org/2000/svg" className="relative top-[1px]">
              <circle cx="22.4229" cy="21.625" r="21.625" fill="#0F98EB"/>
              <rect x="22.1508" y="20.0869" width="21.8965" height="23.1632" fill="#0F98EB"/>
              <ellipse cx="11.0451" cy="17.8474" rx="3.32519" ry="5.18005" fill="white"/>
              <ellipse cx="20.81" cy="17.8474" rx="3.32519" ry="5.18005" fill="white"/>
            </svg>
          </div>
          <div className="space-y-4">
            <h2 className="text-[40px] leading-[48px] font-bold bg-gradient-to-r from-[#08C6C9] to-[#0098EA] bg-clip-text text-transparent">
              Consult from AI Creators
            </h2>
            <p className="text-[#1E293B] text-xl leading-7 max-w-[343px] mx-auto">
              We&apos;ll pick the most relevant creators tailored to your needs
            </p>
          </div>
        </div>
        <SearchInput />
      </div>
      <BottomNav />
    </main>
  )
}

