import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Tasks() {
  const [tasks, setTasks] = useState([])
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }

    const fetchTasks = async () => {
      try {
        const res = await axios.get('http://localhost:8000/tasks', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setTasks(res.data)
      } catch (err) {
        setError('Failed to fetch tasks')
      }
    }

    fetchTasks()
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div>
      <h1>Tasks</h1>
      <button onClick={handleLogout}>Logout</button>
      {error && <p>{error}</p>}
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>{task.title} - {task.status}</li>
        ))}
      </ul>
      {tasks.length === 0 && <p>No tasks yet</p>}
    </div>
  )
}