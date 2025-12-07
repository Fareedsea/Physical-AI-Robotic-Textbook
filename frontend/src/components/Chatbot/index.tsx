const toggleChat = () => setIsOpen(!isOpen);

const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
};
<div className={styles.chatbotWrapper}>
    {/* Chat Window */}
    <div className={clsx(styles.chatWindow, { [styles.open]: isOpen })}>
        <div className={styles.header}>
            <div className={styles.title}>
                <span className={styles.avatar}>🤖</span>
                <span>Physical AI Tutor</span>
            </div>
            <button className={styles.closeBtn} onClick={toggleChat}>×</button>
        </div>

        <div className={styles.messages}>
            {messages.map((msg, idx) => (
                <div key={idx} className={clsx(styles.messageLine, msg.role === 'user' ? styles.userLine : styles.botLine)}>
                    {msg.role === 'assistant' && <div className={styles.messageAvatar}>🤖</div>}
                    <div className={clsx(styles.messageBubble, msg.role === 'user' ? styles.userBubble : styles.botBubble)}>
                        {msg.content}
                    </div>
                </div>
            ))}
            {isLoading && (
                <div className={styles.messageLine}>
                    <div className={styles.messageAvatar}>🤖</div>
                    <div className={clsx(styles.messageBubble, styles.botBubble, styles.loadingBubble)}>
                        <span className={styles.dot}>.</span><span className={styles.dot}>.</span><span className={styles.dot}>.</span>
                    </div>
                </div>
            )}
            <div ref={messagesEndRef} />
        </div>

        <div className={styles.inputArea}>
            <input
                type="text"
                placeholder="Ask a question..."
                className={styles.input}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
            />
            <button className={styles.sendBtn} onClick={handleSend} disabled={isLoading || !input.trim()}>→</button>
        </div>
    </div>

    {/* Floating Toggle Button */}
    <button
        className={clsx(styles.toggleBtn, { [styles.hidden]: isOpen })}
        onClick={toggleChat}
        aria-label="Open Chatbot"
    >
        <span className={styles.toggleIcon}>💬</span>
    </button>
</div>
    );
}
