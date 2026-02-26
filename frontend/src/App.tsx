import SubmitURL from "./components/submitURL";

function App() {
  return (
    <div className='flex flex-col min-h-screen bg-slate-900 text-white items-center p-8'>
      <h1 className='text-3xl font-bold my-3'>
        3D Cloud Generator
      </h1>
      <SubmitURL/>
    </div>
  )
}

export default App;