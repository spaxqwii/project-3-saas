import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post('http://localhost:8000/login', { email, password })
      localStorage.setItem('token', res.data.access_token)
      navigate('/tasks')
    } catch (err) {
      setError('Invalid credentials')
    }
  }

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      {error && <p>{error}</p>}
      <p>No account? <a href="/register">Register</a></p>
    </div>
  )
}