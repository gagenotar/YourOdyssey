import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle, faSpinner, faSearch } from '@fortawesome/free-solid-svg-icons';
import styles from './TravelQA.module.css';

interface TravelQAProps {
  question: string;
  onQuestionChange: (value: string) => void;
  onAskQuestion: () => void;
  answer: string | null;
  askingQuestion: boolean;
}

export function TravelQA({ 
  question, 
  onQuestionChange, 
  onAskQuestion, 
  answer, 
  askingQuestion 
}: TravelQAProps) {
  return (
    <div className={`${styles.qaContainer} container`}>
      <h2 className={styles.qaTitle}>
        <FontAwesomeIcon icon={faQuestionCircle} />
        Ask Travel Questions
      </h2>

      <div className={styles.inputGroup}>
        <input
          type="text"
          value={question}
          onChange={(e) => onQuestionChange(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && onAskQuestion()}
          placeholder="Ask me anything about travel..."
          className={`${styles.input} form-control`}
        />
        <button
          onClick={onAskQuestion}
          disabled={askingQuestion || !question.trim()}
          className={styles.askButton}
        >
          <FontAwesomeIcon icon={askingQuestion ? faSpinner : faSearch} spin={askingQuestion} />
        </button>
      </div>

      {answer && (
        <div className={styles.answerContainer}>
          <div>
            <h3 className={styles.answerTitle}>Answer:</h3>
            <div
              className={styles.answerContent}
              dangerouslySetInnerHTML={{ __html: formatAnswer(answer) }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function escapeHtml(text: string) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatAnswer(answer: string): string {
  // Escape HTML first to avoid XSS.
  let out = escapeHtml(answer);

  // Links: [text](url)
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  // Bold: **text**
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Italic: *text*
  out = out.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Paragraphs and line breaks
  out = out.replace(/\r\n/g, '\n');
  out = out.replace(/\n\n+/g, '</p><p>');
  out = out.replace(/\n/g, '<br>');

  return '<p>' + out + '</p>';
}

