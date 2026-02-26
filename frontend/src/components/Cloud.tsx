import * as THREE from "three"
import { useRef, useState, useMemo, useEffect, Suspense } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Billboard, Text, TrackballControls } from "@react-three/drei"

type WordProps = {
  position: THREE.Vector3
  children: string
  value: number
}

function Word({ children, position, value }: WordProps) {
  const ref = useRef<THREE.Mesh>(null!)
  const [hovered, setHovered] = useState(false)

  useEffect(() => {
    document.body.style.cursor = hovered ? "pointer" : "auto"
    return () => {
      document.body.style.cursor = "auto"
    }
  }, [hovered])

  useFrame(() => {
    if (!ref.current) return

    const material = ref.current.material as THREE.MeshBasicMaterial

    const hue = 2 - value * 2

    const baseColor = new THREE.Color().setHSL(
      hue,
      1,
      0.5
    )

    const hoverColor = new THREE.Color("#fa2720")

    material.color.lerp(
      hovered ? hoverColor : baseColor,
      0.1
    )
  })

  return (
    <Billboard position={position}>
      <Text
        ref={ref}
        fontSize={1 + value * 1.5}
        letterSpacing={-0.05}
        lineHeight={1}
        color="white"
        anchorX="center"
        anchorY="middle"
        onPointerOver={(e) => {
          e.stopPropagation()
          setHovered(true)
        }}
        onPointerOut={() => setHovered(false)}
      >
        {children}
      </Text>
    </Billboard>
  )
}

type CloudGeneratorProps = {
  analysis: Record<string, number>,
  count: number,
  radius: number,
}

function CloudGenerator({
  analysis,
  count = 6, 
  radius = 20 
} : CloudGeneratorProps) {
const words = useMemo(() => {
  const temp: [THREE.Vector3, string, number][] = []
  const spherical = new THREE.Spherical()
  const entries = Object.entries(analysis)

  const phiSpan = Math.PI / (count + 1)
  const thetaSpan = (Math.PI * 2) / count

  entries.forEach(([word, value], idx) => {
    const i = Math.floor(idx / count) + 1
    const j = idx % count

    const position = new THREE.Vector3().setFromSpherical(
      spherical.set(radius, phiSpan * i, thetaSpan * j)
    )

    temp.push([position, word, value])
  })

  return temp
}, [analysis, count, radius])

  return (
    <>
      {words.map(([pos, word, val], i) => (
        <Word key={i} position={pos} value={val}>
          {word}
        </Word>
      ))}
    </>
  )
}

type CloudProps = {
  analysis: Record<string, number>
}

function Cloud({analysis}: CloudProps) {
  const wordCount = Object.keys(analysis).length
  const count = Math.ceil(Math.sqrt(wordCount))


  return (
    <div className="flex-1 w-full" style={{height: '80vh'}}>
      <Canvas
        dpr={[1, 2]}
        camera={{ position: [0, 0, 35], fov: 75 }}
      >
        <fog attach="fog" args={["#202025", 0, 80]} />

        <Suspense fallback={null}>
          <group rotation={[0.3, 0.5, 0]}>
            <CloudGenerator analysis={analysis} count={count} radius={20} />
          </group>
        </Suspense>

        <TrackballControls />
      </Canvas>
    </div>
  )
}

export default Cloud