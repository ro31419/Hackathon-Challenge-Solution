import React, { useState } from 'react';
import { Mic, StopCircle, Volume2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

const FrenchLearningInterface = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [score, setScore] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [response, setResponse] = useState(null);

  const startRecording = () => {
    setIsRecording(true);
    // Simulating recording start
    setTimeout(() => {
      document.getElementById('wave-animation').style.display = 'block';
    }, 100);
  };

  const stopRecording = () => {
    setIsRecording(false);
    document.getElementById('wave-animation').style.display = 'none';
    
    // Simulate processing and scoring
    // In a real implementation, this would process actual audio input
    const mockScores = [
      { score: 85, feedback: "Très bien! Votre prononciation est claire.", response: "Je suis d'accord, continuons la conversation!" },
      { score: 92, feedback: "Excellent! Votre accent est presque parfait.", response: "Impressionnant! Vous parlez très bien français." },
      { score: 78, feedback: "Pas mal! Attention à la prononciation du 'r'.", response: "Continuez à pratiquer, vous vous améliorez!" }
    ];
    
    const randomResult = mockScores[Math.floor(Math.random() * mockScores.length)];
    setScore(randomResult.score);
    setFeedback(randomResult.feedback);
    setResponse(randomResult.response);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            Practice Your French
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center space-y-6">
            <div className="text-center mb-4">
              <p className="text-lg mb-2">Speak in French to practice your pronunciation</p>
              <p className="text-sm text-gray-500">Click the microphone to begin</p>
            </div>

            <div className="relative">
              <Button
                size="lg"
                className={`rounded-full p-6 ${isRecording ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'}`}
                onClick={isRecording ? stopRecording : startRecording}
              >
                {isRecording ? (
                  <StopCircle className="h-8 w-8" />
                ) : (
                  <Mic className="h-8 w-8" />
                )}
              </Button>

              {/* Audio wave animation */}
              <div
                id="wave-animation"
                className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 hidden"
              >
                <div className="flex items-center space-x-1">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className="w-1 bg-blue-500 animate-pulse"
                      style={{
                        height: `${Math.random() * 20 + 10}px`,
                        animationDelay: `${i * 0.1}s`
                      }}
                    />
                  ))}
                </div>
              </div>
            </div>

            {score && (
              <div className="w-full space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <span className="text-lg font-semibold">Score:</span>
                  <span className={`text-2xl font-bold ${
                    score >= 90 ? 'text-green-500' : 
                    score >= 80 ? 'text-blue-500' : 
                    'text-yellow-500'
                  }`}>
                    {score}/100
                  </span>
                </div>

                <Alert className="bg-blue-50">
                  <AlertTitle>Feedback</AlertTitle>
                  <AlertDescription>{feedback}</AlertDescription>
                </Alert>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Volume2 className="h-5 w-5" />
                    <span className="font-semibold">Response:</span>
                  </div>
                  <p className="text-gray-700">{response}</p>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FrenchLearningInterface;
