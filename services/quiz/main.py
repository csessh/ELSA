import asyncio
from argparse import ArgumentParser, Namespace
from random import randint

import arrow
import nats
from redis.asyncio import Redis as AsyncRedis


async def callback_handler(msg):
    """
    Callback handler for messages in `Quiz.>` topic.
    This is where quiz master service perform batch updates
    to database to ensure the game history persists.

    This could be done as a batch update for each round.
    """
    await msg.ack()


async def main_coroutine(args: Namespace):
    redis = AsyncRedis.from_url("redis://localhost:6379")
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()

    await js.add_stream(name="livescore", subjects=["LEADERBOARD.*"])
    await js.add_stream(name="quiz", subjects=["QUIZ.*.*.*"])
    await js.subscribe(subject="QUIZ.*.*.*", cb=callback_handler)

    round = 0
    while round < args.rounds:
        round += 1
        await asyncio.sleep(5)  # Sleep between rounds

        for i in range(0, args.players):
            score = randint(1, args.players)
            await redis.zincrby(args.name, value=f"player{i}", amount=score)

            # quiz master service listen to this topic
            # to ensure score updates are persisted in database
            await js.publish(subject=f"QUIZ.{args.name}.{round}.player{i}", payload=str(score).encode())

        # leaderboard service listens to this topic
        # to trigger its update events
        await js.publish(subject=f"LEADERBOARD.{args.name}", payload=str(arrow.now().timestamp()).encode())


if __name__ == "__main__":
    parser = ArgumentParser(prog="ElsaSim", description="Quiz service simulation", epilog="Let it go, let it go")
    parser.add_argument("-name", type=str, help="Quiz session identifier")
    parser.add_argument("-rounds", type=int, help="Number of rounds in a quiz session")
    parser.add_argument("-players", type=int, help="Number of players in a quiz session")
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.run(main_coroutine(args))
