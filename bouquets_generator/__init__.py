import asyncio
import logging
import pathlib
import random
import sys

import aiofiles

from bouquets_generator.structs import BouquetDesign, Bouquet, Flower

logger = logging.getLogger(__name__)


async def bouquet_designs_consumer(
    bouquet_designs_queue: asyncio.Queue,
    flowers_queue: asyncio.Queue,
    bouquets_queue: asyncio.Queue,
):
    """Taking care on bouquets and their state."""
    worker_id = int(random.random() * 1000)
    bd_str = await bouquet_designs_queue.get()
    bd = BouquetDesign.from_str(bd_str)
    logger.info(
        f"Proccesing of a bd {repr(bd_str)} "
        f"started by worker id {repr(worker_id)}..."
    )
    bouquet = Bouquet(name=bd.name, design=bd)
    while True:
        fl_str = await flowers_queue.get()
        logger.debug(
            f"Flower {repr(fl_str)} received by "
            f"worker id {repr(worker_id)}"
        )
        flower = Flower.from_str(fl_str)
        try:
            await bouquet.use(flower)
        except KeyError:
            # if flower is not compatible with the design
            # we put it back to the queue and allow switch the context
            # to another task
            await flowers_queue.put(fl_str)
            logger.debug(f"Flower {repr(fl_str)} returned to the queue")
            await asyncio.sleep(0)
        else:
            if bouquet.is_ready:
                logger.info(
                    f"Bouquet {repr(bouquet.to_str())} produced by worker"
                    f" {repr(worker_id)}"
                )
                bouquet_designs_queue.task_done()
                await bouquets_queue.put(bouquet.to_str())


async def assign_items_to_queues(
    f_path: pathlib.Path, bd_queue: asyncio.Queue, fl_queue: asyncio.Queue
):
    """Sort the content of input file between queues.

    bd_queue - bouquets design queue
    fl_queue - flowers queue

    :param f_path: path to the source file
    :param bd_queue:
    :param fl_queue:
    :return:
    """
    async with aiofiles.open(f_path) as f:
        target_queue = bd_queue
        async for line in f:
            line = line.strip()
            if not line:
                target_queue = fl_queue
            else:
                await target_queue.put(line)


async def write_stream_to_file(f_path, stream: asyncio.Queue):
    async with aiofiles.open(f_path, "w") as f:
        while stream.qsize():
            await f.write(await stream.get() + "\n")
    logger.info(f"Successfuly written to {repr(f_path)}.")


async def app(src: pathlib.Path, target: pathlib.Path, verbose: bool = False):
    """Cli app for generating bouquets from bouquets designs.

    Common abbreviations:
    - bd - bouquets designs
    - fl - flowers
    - b - bouquets

    App implemented with the help of asyncio.Queue(s)

    :param src: path to the source stream of designs
    :param target: path to the file where to write bouquets stream
    :param verbose: add verbosity
    """
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO if not verbose else logging.DEBUG,
        format=">> %(message)s",
    )
    bd_queue = asyncio.Queue()
    fl_queue = asyncio.Queue()
    b_queue = asyncio.Queue()
    logger.info("Queues created")
    asyncio.create_task(assign_items_to_queues(src, bd_queue, fl_queue))
    # Giving some time for the loop to fill the queues with the bds
    await asyncio.sleep(0.01)
    while bd_queue.qsize():
        asyncio.create_task(
            bouquet_designs_consumer(bd_queue, fl_queue, b_queue)
        )
        # release the loop to actually start working on tasks
        await asyncio.sleep(0)
    await bd_queue.join()
    logger.info(f"Success. All bouquets produced!!!")
    await write_stream_to_file(target, b_queue)
