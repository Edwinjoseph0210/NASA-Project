import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import axios from 'axios'
import { Bell, BellOff, MapPin, AlertTriangle, CheckCircle, X } from 'lucide-react'
import toast from 'react-hot-toast'

interface Alert {
  id: string
  location: { latitude: number; longitude: number }
  parameter: string
  threshold: number
  current_value: number
  severity: string
  message: string
  timestamp: string
  expires_at?: string
}

interface AlertSubscription {
  user_id: string
  latitude: number
  longitude: number
  pm25_threshold?: number
  o3_threshold?: number
  no2_threshold?: number
  aqi_threshold?: number
  web_push_enabled: boolean
  email_enabled: boolean
  sms_enabled: boolean
}

const AlertPanel: React.FC = () => {
  const [showSubscriptionForm, setShowSubscriptionForm] = useState(false)
  const [subscription, setSubscription] = useState<AlertSubscription>({
    user_id: 'demo-user',
    latitude: 40.7128,
    longitude: -74.0060,
    pm25_threshold: 35.4,
    o3_threshold: 0.070,
    no2_threshold: 0.100,
    aqi_threshold: 100,
    web_push_enabled: true,
    email_enabled: false,
    sms_enabled: false
  })

  const queryClient = useQueryClient()

  const { data: alertsData, isLoading: alertsLoading } = useQuery(
    'alerts',
    async () => {
      const response = await axios.get('/api/v1/alerts?hours=24')
      return response.data
    },
    {
      refetchInterval: 60000, // Refetch every minute
    }
  )

  const { data: subscriptionsData } = useQuery(
    ['subscriptions', subscription.user_id],
    async () => {
      const response = await axios.get(`/api/v1/alerts/subscribe/${subscription.user_id}`)
      return response.data
    }
  )

  const subscribeMutation = useMutation(
    async (sub: AlertSubscription) => {
      const response = await axios.post('/api/v1/alerts/subscribe', sub)
      return response.data
    },
    {
      onSuccess: () => {
        toast.success('Alert subscription created successfully!')
        queryClient.invalidateQueries(['subscriptions', subscription.user_id])
        setShowSubscriptionForm(false)
      },
      onError: () => {
        toast.error('Failed to create subscription')
      }
    }
  )

  const unsubscribeMutation = useMutation(
    async (subscriptionId: string) => {
      await axios.delete(`/api/v1/alerts/subscribe/${subscriptionId}`)
    },
    {
      onSuccess: () => {
        toast.success('Subscription cancelled')
        queryClient.invalidateQueries(['subscriptions', subscription.user_id])
      },
      onError: () => {
        toast.error('Failed to cancel subscription')
      }
    }
  )

  const testAlertMutation = useMutation(
    async (alertRequest: any) => {
      const response = await axios.post('/api/v1/alerts/test', alertRequest)
      return response.data
    },
    {
      onSuccess: () => {
        toast.success('Test alert sent!')
      },
      onError: () => {
        toast.error('Failed to send test alert')
      }
    }
  )

  const alerts = alertsData || []
  const subscriptions = subscriptionsData?.subscriptions || []

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'good':
        return 'text-green-600 bg-green-100'
      case 'moderate':
        return 'text-yellow-600 bg-yellow-100'
      case 'unhealthy for sensitive groups':
        return 'text-orange-600 bg-orange-100'
      case 'unhealthy':
        return 'text-red-600 bg-red-100'
      case 'very unhealthy':
        return 'text-purple-600 bg-purple-100'
      case 'hazardous':
        return 'text-red-800 bg-red-200'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const handleSubscribe = () => {
    subscribeMutation.mutate(subscription)
  }

  const handleUnsubscribe = (subscriptionId: string) => {
    unsubscribeMutation.mutate(subscriptionId)
  }

  const handleTestAlert = () => {
    testAlertMutation.mutate({
      latitude: subscription.latitude,
      longitude: subscription.longitude,
      parameter: 'aqi',
      threshold: subscription.aqi_threshold,
      message: 'Test alert from AirAware',
      user_id: subscription.user_id
    })
  }

  return (
    <div className="space-y-6">
      {/* Active Alerts */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              Active Alerts ({alerts.length})
            </h3>
            <button
              onClick={handleTestAlert}
              disabled={testAlertMutation.isLoading}
              className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {testAlertMutation.isLoading ? 'Sending...' : 'Send Test Alert'}
            </button>
          </div>
        </div>
        
        <div className="max-h-96 overflow-y-auto">
          {alertsLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-gray-600">Loading alerts...</span>
            </div>
          ) : alerts.length > 0 ? (
            <div className="divide-y divide-gray-200">
              {alerts.map((alert: Alert) => (
                <div key={alert.id} className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <AlertTriangle className="h-5 w-5 text-orange-500 mr-2" />
                        <h4 className="text-sm font-medium text-gray-900">
                          {alert.parameter.toUpperCase()} Alert
                        </h4>
                        <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                          {alert.severity}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{alert.message}</p>
                      <div className="flex items-center text-xs text-gray-500">
                        <MapPin className="h-3 w-3 mr-1" />
                        {alert.location.latitude.toFixed(4)}, {alert.location.longitude.toFixed(4)}
                        <span className="mx-2">•</span>
                        {new Date(alert.timestamp).toLocaleString()}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-semibold text-gray-900">
                        {alert.current_value.toFixed(1)}
                      </div>
                      <div className="text-sm text-gray-600">
                        Threshold: {alert.threshold}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <CheckCircle className="h-8 w-8 mx-auto mb-2 text-green-400" />
              <p className="text-sm">No active alerts</p>
              <p className="text-xs text-gray-400 mt-1">Air quality conditions are within normal ranges</p>
            </div>
          )}
        </div>
      </div>

      {/* Alert Subscriptions */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              My Alert Subscriptions ({subscriptions.length})
            </h3>
            <button
              onClick={() => setShowSubscriptionForm(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              <Bell className="h-4 w-4 mr-2 inline" />
              Subscribe to Alerts
            </button>
          </div>
        </div>
        
        <div className="p-6">
          {subscriptions.length > 0 ? (
            <div className="space-y-4">
              {subscriptions.map((sub: any) => (
                <div key={sub.id} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <MapPin className="h-4 w-4 text-gray-500 mr-2" />
                        <span className="text-sm font-medium text-gray-900">
                          {sub.latitude.toFixed(4)}, {sub.longitude.toFixed(4)}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                        {sub.pm25_threshold && (
                          <div>PM2.5: {sub.pm25_threshold} μg/m³</div>
                        )}
                        {sub.o3_threshold && (
                          <div>O3: {sub.o3_threshold} ppb</div>
                        )}
                        {sub.no2_threshold && (
                          <div>NO2: {sub.no2_threshold} ppb</div>
                        )}
                        {sub.aqi_threshold && (
                          <div>AQI: {sub.aqi_threshold}</div>
                        )}
                      </div>
                      <div className="flex items-center mt-2 space-x-4 text-xs text-gray-500">
                        <div className="flex items-center">
                          <Bell className="h-3 w-3 mr-1" />
                          Web Push: {sub.web_push_enabled ? 'On' : 'Off'}
                        </div>
                        <div className="flex items-center">
                          <BellOff className="h-3 w-3 mr-1" />
                          Email: {sub.email_enabled ? 'On' : 'Off'}
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => handleUnsubscribe(sub.id)}
                      disabled={unsubscribeMutation.isLoading}
                      className="p-1 text-gray-400 hover:text-red-600"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Bell className="h-8 w-8 mx-auto mb-2 text-gray-400" />
              <p className="text-sm">No alert subscriptions</p>
              <p className="text-xs text-gray-400 mt-1">Subscribe to get notified about air quality changes</p>
            </div>
          )}
        </div>
      </div>

      {/* Subscription Form Modal */}
      {showSubscriptionForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Subscribe to Alerts</h3>
              <button
                onClick={() => setShowSubscriptionForm(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    step="0.0001"
                    placeholder="Latitude"
                    value={subscription.latitude}
                    onChange={(e) => setSubscription({
                      ...subscription,
                      latitude: parseFloat(e.target.value) || 0
                    })}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                  <input
                    type="number"
                    step="0.0001"
                    placeholder="Longitude"
                    value={subscription.longitude}
                    onChange={(e) => setSubscription({
                      ...subscription,
                      longitude: parseFloat(e.target.value) || 0
                    })}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Alert Thresholds
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    step="0.1"
                    placeholder="PM2.5 (μg/m³)"
                    value={subscription.pm25_threshold || ''}
                    onChange={(e) => setSubscription({
                      ...subscription,
                      pm25_threshold: parseFloat(e.target.value) || undefined
                    })}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                  <input
                    type="number"
                    step="0.001"
                    placeholder="O3 (ppb)"
                    value={subscription.o3_threshold || ''}
                    onChange={(e) => setSubscription({
                      ...subscription,
                      o3_threshold: parseFloat(e.target.value) || undefined
                    })}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                  <input
                    type="number"
                    step="0.001"
                    placeholder="NO2 (ppb)"
                    value={subscription.no2_threshold || ''}
                    onChange={(e) => setSubscription({
                      ...subscription,
                      no2_threshold: parseFloat(e.target.value) || undefined
                    })}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                  <input
                    type="number"
                    placeholder="AQI"
                    value={subscription.aqi_threshold || ''}
                    onChange={(e) => setSubscription({
                      ...subscription,
                      aqi_threshold: parseInt(e.target.value) || undefined
                    })}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notification Methods
                </label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={subscription.web_push_enabled}
                      onChange={(e) => setSubscription({
                        ...subscription,
                        web_push_enabled: e.target.checked
                      })}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Web Push Notifications</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={subscription.email_enabled}
                      onChange={(e) => setSubscription({
                        ...subscription,
                        email_enabled: e.target.checked
                      })}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Email Notifications</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={subscription.sms_enabled}
                      onChange={(e) => setSubscription({
                        ...subscription,
                        sms_enabled: e.target.checked
                      })}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">SMS Notifications</span>
                  </label>
                </div>
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowSubscriptionForm(false)}
                className="px-4 py-2 text-sm text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                onClick={handleSubscribe}
                disabled={subscribeMutation.isLoading}
                className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {subscribeMutation.isLoading ? 'Creating...' : 'Subscribe'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AlertPanel
