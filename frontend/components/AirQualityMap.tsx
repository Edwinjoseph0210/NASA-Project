import React, { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

interface AirQualityMapProps {
  onLocationSelect: (location: { latitude: number; longitude: number; name?: string }) => void
  selectedLocation?: { latitude: number; longitude: number; name?: string } | null
}

const AirQualityMap: React.FC<AirQualityMapProps> = ({ onLocationSelect, selectedLocation }) => {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [mapLoaded, setMapLoaded] = useState(false)

  useEffect(() => {
    if (!mapContainer.current) return

    // Initialize map
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v10',
      center: [-98.5795, 39.8283], // Center of USA
      zoom: 4,
      maxZoom: 18
    })

    map.current.on('load', () => {
      setMapLoaded(true)
      
      // Add heatmap layer for air quality data
      if (map.current) {
        map.current.addSource('air-quality', {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: []
          }
        })

        map.current.addLayer({
          id: 'air-quality-heatmap',
          type: 'heatmap',
          source: 'air-quality',
          maxzoom: 15,
          paint: {
            'heatmap-weight': [
              'interpolate',
              ['linear'],
              ['get', 'aqi'],
              0, 0,
              50, 0.2,
              100, 0.4,
              150, 0.6,
              200, 0.8,
              300, 1
            ],
            'heatmap-intensity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 1,
              15, 3
            ],
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0, 'rgba(0, 228, 0, 0)',
              0.1, 'rgba(0, 228, 0, 1)',
              0.2, 'rgba(255, 255, 0, 1)',
              0.3, 'rgba(255, 126, 0, 1)',
              0.4, 'rgba(255, 0, 0, 1)',
              0.5, 'rgba(143, 63, 151, 1)',
              1, 'rgba(126, 0, 35, 1)'
            ],
            'heatmap-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              0, 2,
              15, 20
            ],
            'heatmap-opacity': [
              'interpolate',
              ['linear'],
              ['zoom'],
              7, 1,
              15, 0
            ]
          }
        })

        // Add click handler
        map.current.on('click', (e) => {
          const { lng, lat } = e.lngLat
          onLocationSelect({ latitude: lat, longitude: lng })
        })

        // Add cursor pointer on hover
        map.current.on('mouseenter', 'air-quality-heatmap', () => {
          if (map.current) {
            map.current.getCanvas().style.cursor = 'pointer'
          }
        })

        map.current.on('mouseleave', 'air-quality-heatmap', () => {
          if (map.current) {
            map.current.getCanvas().style.cursor = ''
          }
        })
      }
    })

    return () => {
      if (map.current) {
        map.current.remove()
      }
    }
  }, [])

  useEffect(() => {
    if (mapLoaded && selectedLocation && map.current) {
      // Add marker for selected location
      new mapboxgl.Marker({ color: '#3B82F6' })
        .setLngLat([selectedLocation.longitude, selectedLocation.latitude])
        .addTo(map.current)

      // Center map on selected location
      map.current.flyTo({
        center: [selectedLocation.longitude, selectedLocation.latitude],
        zoom: 10
      })
    }
  }, [selectedLocation, mapLoaded])

  return (
    <div className="w-full h-96 rounded-lg overflow-hidden">
      <div ref={mapContainer} className="w-full h-full" />
      
      {/* Map Controls */}
      <div className="absolute top-4 right-4 space-y-2">
        <div className="bg-white rounded-lg shadow-lg p-3">
          <h4 className="text-sm font-medium text-gray-900 mb-2">AQI Legend</h4>
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
            <div className="flex items-center">
              <div className="w-3 h-3 bg-purple-500 rounded mr-2"></div>
              <span>Very Unhealthy (201-300)</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-800 rounded mr-2"></div>
              <span>Hazardous (301+)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-3">
        <p className="text-sm text-gray-600">
          Click anywhere on the map to view air quality data for that location
        </p>
      </div>
    </div>
  )
}

export default AirQualityMap
