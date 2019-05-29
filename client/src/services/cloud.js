import { cloud as api } from '@/services/api'

export default {
    status () {
      return api().get('status')
    },
  
    open () {
      return api().get('open')
    },
  
    close () {
      return api().get('close')
    },
  
    data () {
      return api().get('data').then((response) => {
          let data = response.data.split(',')
          return {
              gas: data[0],
              sound: data[1],
              humidity: data[2],
              temp: data[3]
          }
      })
    }
  }
  