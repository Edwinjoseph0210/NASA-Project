import React, { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

interface KeralaMapProps {
  onLocationSelect: (location: { latitude: number; longitude: number; name?: string }) => void
  selectedLocation: { latitude: number; longitude: number; name?: string }
  center: { latitude: number; longitude: number; name?: string }
}

const KeralaMap: React.FC<KeralaMapProps> = ({ onLocationSelect, selectedLocation, center }) => {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [mapLoaded, setMapLoaded] = useState(false)

  // Kerala monitoring stations
  const keralaStations = [
    { id: 'KT001', name: 'Kottayam Medical College', lat: 9.5956, lon: 76.5214, aqi: 48 },
    { id: 'KT002', name: 'Kottayam Railway Station', lat: 9.5900, lon: 76.5200, aqi: 52 },
    { id: 'KT003', name: 'Kottayam Bus Stand', lat: 9.6000, lon: 76.5300, aqi: 45 },
    { id: 'KT004', name: 'Kottayam Industrial Area', lat: 9.5800, lon: 76.5100, aqi: 65 },
    { id: 'KT005', name: 'Kottayam Residential', lat: 9.6100, lon: 76.5400, aqi: 42 },
    { id: 'KT006', name: 'Ernakulam Central', lat: 9.9312, lon: 76.2673, aqi: 58 },
    { id: 'KT007', name: 'Thrissur Central', lat: 10.5276, lon: 76.2144, aqi: 55 },
    { id: 'KT008', name: 'Alappuzha Central', lat: 9.4981, lon: 76.3388, aqi: 49 }
  ]

  useEffect(() => {
    if (!mapContainer.current) return

    // Initialize map focused on Kerala
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v10',
      center: [center.longitude, center.latitude],
      zoom: 10,
      maxZoom: 18
    })

    map.current.on('load', () => {
      setMapLoaded(true)
      
      // Add station markers
      keralaStations.forEach(station => {
        const color = getAQIColor(station.aqi)
        
        // Create marker element
        const el = document.createElement('div')
        el.className = 'station-marker'
        el.style.width = '20px'
        el.style.height = '20px'
        el.style.borderRadius = '50%'
        el.style.backgroundColor = color
        el.style.border = '2px solid white'
        el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)'
        el.style.cursor = 'pointer'
        
        // Add marker to map
        new mapboxgl.Marker(el)
          .setLngLat([station.lon, station.lat])
          .setPopup(
            new mapboxgl.Popup({ offset: 25 })
              .setHTML(`
                <div class="p-2">
                  <h3 class="font-semibold text-sm">${station.name}</h3>
                  <p class="text-xs text-gray-600">AQI: ${station.aqi}</p>
                  <p class="text-xs text-gray-600">${getAQILabel(station.aqi)}</p>
                </div>
              `)
          )
          .addTo(map.current!)
        
        // Add click handler
        el.addEventListener('click', () => {
          onLocationSelect({
            latitude: station.lat,
            longitude: station.lon,
            name: station.name
          })
        })
      })

      // Add click handler for map
      map.current.on('click', (e) => {
        const { lng, lat } = e.lngLat
        onLocationSelect({ latitude: lat, longitude: lng })
      })
    })

    return () => {
      if (map.current) {
        map.current.remove()
      }
    }
  }, [])

  useEffect(() => {
    if (mapLoaded && selectedLocation && map.current) {
      // Center map on selected location
      map.current.flyTo({
        center: [selectedLocation.longitude, selectedLocation.latitude],
        zoom: 12
      })
    }
  }, [selectedLocation, mapLoaded])

  const getAQIColor = (aqi: number) => {
    if (aqi <= 50) return '#00e400'
    if (aqi <= 100) return '#ffff00'
    if (aqi <= 150) return '#ff7e00'
    if (aqi <= 200) return '#ff0000'
    if (aqi <= 300) return '#8f3f97'
    return '#7e0023'
  }

  const getAQILabel = (aqi: number) => {
    if (aqi <= 50) return 'Good'
    if (aqi <= 100) return 'Moderate'
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups'
    if (aqi <= 200) return 'Unhealthy'
    if (aqi <= 300) return 'Very Unhealthy'
    return 'Hazardous'
  }

  return (
    <div className="w-full h-96 rounded-lg overflow-hidden">
      <div ref={mapContainer} className="w-full h-full" />
      
      {/* Map Controls */}
      <div className="absolute top-4 right-4 space-y-2">
        <div className="bg-white rounded-lg shadow-lg p-3">
          <h4 className="text-sm font-medium text-gray-900 mb-2">🌴 Kerala AQI Legend</h4>
          <div className="space-y-1 text-xs">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
              <span>Good (0-50)</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-yellow-500 rounded mr-2"></div>
              <span>Moderate (51-100)</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-orange-500 rounded mr-2"></div>
              <span>Unhealthy for Sensitive Groups (101-150)</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-500 rounded mr-2"></div>
              <span>Unhealthy (151-200)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-3">
        <p className="text-sm text-gray-600">
          🗺️ Click on stations or anywhere on the map to view air quality data
        </p>
      </div>

      {/* Kerala Info */}
      <div className="absolute top-4 left-4 bg-white rounded-lg shadow-lg p-3">
        <h4 className="text-sm font-medium text-gray-900 mb-1">🌴 Kerala Air Quality</h4>
        <p className="text-xs text-gray-600">Monitoring {keralaStations.length} stations</p>
        <p className="text-xs text-gray-600">Current average AQI: 52 (Good)</p>
      </div>
    </div>
  )
}

export default KeralaMap
