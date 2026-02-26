import * as THREE from "three"
import { useRef, useState, useMemo, useEffect, Suspense } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Billboard, Text, TrackballControls } from "@react-three/drei"

type WordProps = {
  position: THREE.Vector3
  children: string
}

function Word({ children, position }: WordProps) {
  const ref = useRef<THREE.Mesh>(null!)
  const [hovered, setHovered] = useState(false)

  const color = new THREE.Color()

  useEffect(() => {
    document.body.style.cursor = hovered ? "pointer" : "auto"
    return () => {
      document.body.style.cursor = "auto"
    }
  }, [hovered])

  useFrame(() => {
    if (!ref.current) return

    const material = ref.current.material as THREE.MeshBasicMaterial
    material.color.lerp(
      color.set(hovered ? "#fa2720" : "#ffffff"),
      0.1
    )
  })

  return (
    <Billboard position={position}>
      <Text
        ref={ref}
        fontSize={2.5}
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
    const temp: [THREE.Vector3, string][] = []
    const spherical = new THREE.Spherical()
    const entries = Object.keys(analysis)

    const phiSpan = Math.PI / (count + 1)
    const thetaSpan = (Math.PI * 2) / count

    for (let i = 1; i < count + 1; i++) {
      for (let j = 0; j < count; j++) {
        const position = new THREE.Vector3().setFromSpherical(
          spherical.set(radius, phiSpan * i, thetaSpan * j)
        )
        
        const word = entries[i * count + j]
        if (word) temp.push([position, word])
      }
    }

    return temp
  }, [count, radius])

  return (
    <>
      {words.map(([pos, word], i) => (
        <Word key={i} position={pos}>
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
  return (
    <div className="w-screen h-screen">
      <Canvas
        dpr={[1, 2]}
        camera={{ position: [0, 0, 35], fov: 75 }}
      >
        <fog attach="fog" args={["#202025", 0, 80]} />

        <Suspense fallback={null}>
          <group rotation={[0.3, 0.5, 0]}>
            <CloudGenerator analysis={analysis} count={8} radius={20} />
          </group>
        </Suspense>

        <TrackballControls />
      </Canvas>
    </div>
  )
}

export default Cloud