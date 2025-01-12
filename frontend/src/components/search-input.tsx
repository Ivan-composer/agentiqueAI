'use client'

import { useState } from 'react'

export default function SearchInput() {
  const [isFocused, setIsFocused] = useState(false)
  const [value, setValue] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (value.trim()) {
      console.log('Search value:', value)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full relative drop-shadow-lg">
      <div
        className={`absolute inset-0 rounded-[100px] bg-gradient-to-r from-[#08C6C9] to-[#0098EA] ${
          isFocused ? 'opacity-100' : 'opacity-50'
        }`}
        style={{ padding: '1.5px' }}
      >
        <div className="absolute inset-0 bg-white rounded-[100px]" />
      </div>
      <div className="relative flex items-center">
        <input
          type="text"
          placeholder="Ask for anything"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className="w-full h-[56px] px-6 rounded-[100px] bg-transparent border-none outline-none text-[#1E293B] placeholder-[#08C6C9] text-[17px] font-medium"
        />
        <button 
          type="submit" 
          className="absolute right-1 bg-gradient-to-r from-[#08C6C9] to-[#0098EA] text-white px-4 py-1.5 rounded-[100px] flex items-center gap-1.5 drop-shadow-sm"
        >
          <svg width="16" height="16" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M25.5242 11.3586C25.5256 11.0658 25.6188 10.7809 25.7907 10.5439C25.9626 10.307 26.2046 10.13 26.4824 10.0378L29.9526 8.87244C31.0211 8.52314 31.995 7.93272 32.7988 7.14687C33.6026 6.36101 34.2149 5.40078 34.5882 4.34045L35.7536 0.870243C35.8585 0.612958 36.0378 0.392772 36.2684 0.237775C36.499 0.0827788 36.7706 0 37.0484 0C37.3263 0 37.5979 0.0827788 37.8285 0.237775C38.0591 0.392772 38.2383 0.612958 38.3433 0.870243L39.5605 4.34045C39.9202 5.41995 40.5264 6.40085 41.331 7.20545C42.1356 8.01005 43.1165 8.61624 44.196 8.97603L47.6662 10.1414C47.9235 10.2463 48.1437 10.4256 48.2987 10.6562C48.4537 10.8868 48.5365 11.1584 48.5365 11.4362C48.5365 11.7141 48.4537 11.9857 48.2987 12.2163C48.1437 12.4469 47.9235 12.6262 47.6662 12.7311L44.196 13.8965C43.1165 14.2563 42.1356 14.8625 41.331 15.6671C40.5264 16.4717 39.9202 17.4525 39.5605 18.532L38.3951 22.0023C38.2901 22.2595 38.1109 22.4797 37.8803 22.6347C37.6497 22.7897 37.3781 22.8725 37.1002 22.8725C36.8224 22.8725 36.5508 22.7897 36.3202 22.6347C36.0896 22.4797 35.9103 22.2595 35.8054 22.0023L34.64 18.532C34.2802 17.4525 33.674 16.4717 32.8694 15.6671C32.0648 14.8625 31.0839 14.2563 30.0044 13.8965L26.5342 12.7311C26.2382 12.6456 25.9787 12.4646 25.796 12.2164C25.6134 11.9682 25.5178 11.6667 25.5242 11.3586ZM1.1551 29.3052L5.06556 28.0104C6.27093 27.607 7.36615 26.9291 8.26495 26.0304C9.16374 25.1316 9.84155 24.0363 10.245 22.831L11.5398 18.9205C11.6354 18.5998 11.832 18.3185 12.1003 18.1186C12.3686 17.9186 12.6943 17.8105 13.0289 17.8105C13.3635 17.8105 13.6892 17.9186 13.9575 18.1186C14.2258 18.3185 14.4224 18.5998 14.518 18.9205L15.8128 22.831C16.2163 24.0363 16.8941 25.1316 17.7929 26.0304C18.6917 26.9291 19.7869 27.607 20.9923 28.0104L24.9027 29.3052C25.2234 29.4008 25.5047 29.5974 25.7047 29.8657C25.9047 30.134 26.0127 30.4597 26.0127 30.7943C26.0127 31.1289 25.9047 31.4546 25.7047 31.7229C25.5047 31.9912 25.2234 32.1878 24.9027 32.2834L20.9923 33.5782C19.7869 33.9817 18.6917 34.6595 17.7929 35.5583C16.8941 36.4571 16.2163 37.5523 15.8128 38.7577L14.518 42.6681C14.4224 42.9888 14.2258 43.2701 13.9575 43.4701C13.6892 43.6701 13.3635 43.7781 13.0289 43.7781C12.6943 43.7781 12.3686 43.6701 12.1003 43.4701C11.832 43.2701 11.6354 42.9888 11.5398 42.6681L10.245 38.7577C9.84155 37.5523 9.16374 36.4571 8.26495 35.5583C7.36615 34.6595 6.27093 33.9817 5.06556 33.5782L1.1551 32.2834C0.834408 32.1878 0.553143 31.9912 0.353151 31.7229C0.15316 31.4546 0.0451254 31.1289 0.0451254 30.7943C0.0451254 30.4597 0.15316 30.134 0.353151 29.8657C0.553143 29.5974 0.834408 29.4008 1.1551 29.3052ZM31.636 45.1283L36.8154 43.445C38.39 42.9216 39.8209 42.0381 40.9942 40.8647C42.1676 39.6914 43.0511 38.2605 43.5745 36.6859L45.2578 31.5065C45.3987 31.1073 45.6598 30.7616 46.0054 30.5171C46.3509 30.2726 46.7638 30.1412 47.1872 30.1412C47.6105 30.1412 48.0234 30.2726 48.3689 30.5171C48.7145 30.7616 48.9757 31.1073 49.1165 31.5065L50.7998 36.6859C51.3128 38.2495 52.1805 39.6732 53.3351 40.8458C54.4897 42.0183 55.8999 42.9079 57.4553 43.445L62.6348 45.1283C63.034 45.2692 63.3796 45.5304 63.6242 45.8759C63.8687 46.2215 64 46.6344 64 47.0577C64 47.481 63.8687 47.8939 63.6242 48.2394C63.3796 48.585 63.034 48.8462 62.6348 48.987L57.4553 50.6703C55.8779 51.1963 54.4453 52.0838 53.2717 53.2618C52.0982 54.4399 51.2162 55.8759 50.6962 57.4553L49.0129 62.6348C48.8721 63.034 48.6109 63.3797 48.2653 63.6242C47.9198 63.8687 47.5069 64 47.0836 64C46.6603 64 46.2474 63.8687 45.9018 63.6242C45.5563 63.3797 45.2951 63.034 45.1542 62.6348L43.4709 57.4553C42.9475 55.8807 42.064 54.4499 40.8906 53.2765C39.7173 52.1032 38.2864 51.2197 36.7118 50.6962L31.5324 49.0129C31.1332 48.8721 30.7875 48.6109 30.543 48.2653C30.2984 47.9198 30.1671 47.5069 30.1671 47.0836C30.1671 46.6603 30.2984 46.2474 30.543 45.9018C30.7875 45.5563 31.1332 45.2951 31.5324 45.1542L31.636 45.1283Z" fill="currentColor"/>
          </svg>
          <span className="text-sm font-semibold">PRO</span>
        </button>
      </div>
    </form>
  )
}

