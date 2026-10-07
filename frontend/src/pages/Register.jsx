import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Register() {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleRegister = async (e) => {
    e.preventDefault()
    try {
      await axios.post('http://localhost:8000/register', { email, username, password })
      navigate('/login')
    } catch (err) {
      setError('Registration failed')
    }
  }

  return (
    <div>
      <h1>Register</h1>
      <form onSubmit={handleRegister}>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
      {error && <p>{error}</p>}
      <p>Already have account? <a href="/login">Login</a></p>
    </div>
  )
}