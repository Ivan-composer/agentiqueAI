interface QuestIconProps {
  className?: string
}

export default function QuestIcon({ className = "w-6 h-6" }: QuestIconProps) {
  return (
    <svg className={className} viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="120" height="120" rx="24" fill="url(#paint0_linear_2019_2979)"/>
      <path d="M78.3419 29.2278C78.646 28.9219 79.139 28.9219 79.4431 29.2278L80.9952 30.789C84.6995 34.5151 90.7055 34.5151 94.4099 30.789C94.6569 30.5406 95.0573 30.5406 95.3043 30.789L103.577 39.1102C103.824 39.3586 103.824 39.7614 103.577 40.0098C99.8726 43.7359 99.8726 49.7771 103.577 53.5032L105.293 55.2291C105.603 55.541 105.603 56.0468 105.293 56.3588L87 74.5L60 47.5001L78.3419 29.2278Z" fill="url(#paint1_linear_2019_2979)"/>
      <path fillRule="evenodd" clipRule="evenodd" d="M14.8472 55.0533C14.5431 55.3602 14.5431 55.8579 14.8472 56.1648L33.1656 74.6576L53.8065 95.495C57.294 99.0157 62.9484 99.0157 66.4358 95.495L87.0768 74.6575L60.1212 47.4454V47.4452L60.1211 47.4453L41.8137 28.9635C41.5036 28.6505 41.0009 28.6505 40.6908 28.9635L38.985 30.6856C35.2762 34.4297 29.263 34.4297 25.5542 30.6856C25.3069 30.436 24.906 30.436 24.6588 30.6856L16.3893 39.0338C16.142 39.2835 16.142 39.6882 16.3893 39.9378C20.0981 43.6819 20.0981 49.7524 16.3892 53.4965L14.8472 55.0533Z" fill="url(#paint2_linear_2019_2979)"/>
      <defs>
        <linearGradient id="paint0_linear_2019_2979" x1="0" y1="0" x2="120" y2="120" gradientUnits="userSpaceOnUse">
          <stop stopColor="#27BDFE"/>
          <stop offset="1" stopColor="#0882E7"/>
        </linearGradient>
        <linearGradient id="paint1_linear_2019_2979" x1="98.5843" y1="21.5779" x2="80.5289" y2="67.0646" gradientUnits="userSpaceOnUse">
          <stop stopColor="white" stopOpacity="0.32"/>
          <stop offset="1" stopColor="white" stopOpacity="0.8"/>
        </linearGradient>
        <linearGradient id="paint2_linear_2019_2979" x1="82.9359" y1="73.8028" x2="16.2176" y2="33.8014" gradientUnits="userSpaceOnUse">
          <stop stopColor="white"/>
          <stop offset="1" stopColor="white" stopOpacity="0.4"/>
        </linearGradient>
      </defs>
    </svg>
  )
}

