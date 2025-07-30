### Common messages ###
attention-message = Attention, { $recipient_name }!
    { $initiator_name ->
        [null] { "" }
       *[other] { $initiator_name } { $initiator_username ->
            [null] { "" }
           *[other] (@{ $initiator_username })
        }
    } { $text }

subscribe = subscribed to you
unsubscribe = unsubscribed from you

add_to_lecture = added you to the lecture
remove_from_lecture = removed you from the lecture

welcome-notification =
    Hello, { $first_name } { $last_name ->
        [null] { "" }
       *[other] { $last_name }
    }{ $username ->
        [null] { "" }
       *[other] (@{ $username })
    }!

### Conference notifications ###
conference-notification =
    { $text }?token={ $token }'>Click to join</a>.
    Lecture: <b>{ $lecture_name }</b>.
    Starts in: { $time_to_start }

conference-invitation =
    You're invited to a conference!
    Date: <b>{ $date }</b> at <b>{ $time }</b>
    Speaker: { $speaker_name } { $speaker_username ->
        [null] { "" }
       *[other] (@{ $speaker_username })
    }
    Duration: <b>{ $duration } minutes</b>
    Link: <a href='{ $link }

### Time formats ###
time-duration =
    { $days ->
        [0] { "" }
        [1] 1 day
       *[other] { $days } days
    } { $hours ->
        [0] { $minutes } min
        [1] 1 hour { $minutes } min
       *[other] { $hours } hours { $minutes } min
    }
