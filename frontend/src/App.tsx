
import { LeftMenu } from './components/templates/left-menu/left-menu'
import { RightMenu } from './components/templates/right-menu/right-menu'

export default function App() {
  return (
    <div className='bg-stone-900 h-screen'>
      <div className='flex justify-between'>
        <LeftMenu />
        <div></div>
        <RightMenu />
      </div>
    </div>
  )
}


