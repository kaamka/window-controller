import { cloud as api, arduinoID as id } from '@/services/api'

export default {
    status () {
      return api().get(`data/latest/status/${id}`)
    },
  
    open () {
      return api().get(`open/${id}`)
    },
  
    close () {
      return api().get(`close/${id}`)
    },
  
    data () {
      return api().get(`data/latest/${id}`).then((response) => {
          let data = response.data
          return {
              gas: data.gas,
              sound: data.sound,
              humidity: data.hum,
              temp: data.temp
          }
      })
    },
    allData () {
      return api().get(`data/all/${id}`)
    },
    devices () {
      return api().get('devices').then(response => response.data)
    }
  }
  