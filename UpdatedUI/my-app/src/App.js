import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  TextField,
  MenuItem,
  Button,
  CircularProgress,
} from '@mui/material';
import InputAdornment from '@mui/material/InputAdornment';
import axios from 'axios';
import './App.css';

const App = () => {
  const [weather, setWeather] = useState('');
  const [temperature, setTemperature] = useState('');
  const [event, setEvent] = useState('');
  const [dayOfWeek, setDayOfWeek] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!weather || !event || !dayOfWeek || !temperature) {
      alert('Please fill out all fields.');
      return;
    }

    setLoading(true);

    const data = JSON.stringify({
      weather,
      temperature,
      event,
      day_of_week: dayOfWeek,
    });

    console.log(data);
    
    const config = {
      method: 'post',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/predict',
      headers: { 
        'Content-Type': 'application/json'
      },
      data : data
    }

    axios.request(config)
    .then((response) => {
      console.log(JSON.stringify(response.data));
      setPrediction(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
      
    setLoading(false);
  };

  return (
    <Container>
      <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
        <Typography variant="h4" gutterBottom>
          Attendance Prediction
        </Typography>
        <Grid container spacing={3}>
          {/* Weather and Temperature */}
          <Grid item xs={9}>
            <TextField
              label="Weather"
              select
              fullWidth
              value={weather}
              onChange={(e) => setWeather(e.target.value)}
            >
              {['Sunny', 'Rainy', 'Cloudy'].map((option) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={3}>
            <TextField
              placeholder="Temperature"
              type="number"
              fullWidth
              value={temperature}
              onChange={(e) => setTemperature(e.target.value)}
              InputProps={{
                endAdornment: <InputAdornment position="end">°F</InputAdornment>,
                style: { textAlign: 'center' },
              }}
            />
          </Grid>

          {/* Event */}
          <Grid item xs={12}>
            <TextField
              label="Event"
              select
              fullWidth
              value={event}
              onChange={(e) => setEvent(e.target.value)}
            >
              {['Sports', 'Concert', 'Conference'].map((option) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          {/* Day of the Week */}
          <Grid item xs={12}>
            <TextField
              label="Day of the Week"
              select
              fullWidth
              value={dayOfWeek}
              onChange={(e) => setDayOfWeek(e.target.value)}
            >
              {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map(
                (option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                )
              )}
            </TextField>
          </Grid>

          {/* Predict Button */}
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Predict Attendance'}
            </Button>
          </Grid>

          {/* Prediction Result */}
          {prediction !== null && (
            <Grid item xs={12}>
              <Typography variant="h6">
                Predicted Attendance: {prediction}
              </Typography>
            </Grid>
          )}
        </Grid>
      </Paper>
    </Container>
  );
};

export default App;