import unittest
from mychain import Transaction, Block, validatechain
from mychain import hash_message


class TestHashing(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(hash_message("Test"), hash_message("Test"))

    def test_hash_not_equeal(self):
        self.assertNotEquals(hash_message("Test"), hash_message("test"))


class TransactionTest(unittest.TestCase):

    def setUp(self):
        self.tx = Transaction("Satheesh", "Chaitra", 10)

    def test_new_transaction(self):
        self.assertEqual(self.tx.amount, 10)
        self.assertEqual(self.tx.sender, "Satheesh")
        self.assertEqual(self.tx.receiver, "Chaitra")


class BlockTest(unittest.TestCase):

    def setUp(self):
        self.tx = Transaction("Satheesh", "Chaitra", 10)
        self.newtx = Transaction("Chaitra", "Nala", 10)
        self.block = Block()

    def test_add_block(self):
        self.assertEqual(self.block.transaction_count, 0)
        self.block.add_transaction(self.tx)
        self.assertEqual(self.block.transaction_count, 1)

    def test_not_final(self):
        self.assertFalse(self.block.validate())
        self.assertIsNone(self.block.hash)

    def test_finalize(self):
        self.assertFalse(self.block.validate())
        self.block.finalize()
        self.assertIsNotNone(self.block.hash)
        self.assertIsNone(self.block.prev_hash)
        self.assertEqual(self.block.height, 1)
        self.assertTrue(self.block.validate())

    def test_finalize_twice(self):
        self.block.finalize()
        with self.assertRaises(ValueError):
            self.block.finalize()

    def test_finalize_false(self):
        self.assertFalse(self.block.validate())
        self.assertIsNone(self.block.hash)
        self.block.finalize()
        old_hash = self.block.hash
        self.assertTrue(self.block.validate())
        self.block.add_transaction(self.newtx)
        with self.assertRaises(ValueError):
            self.block.finalize()
        new_hash = self.block.hash
        self.assertEqual(old_hash, new_hash)
        self.assertFalse(self.block.validate())


class BlockChainTest(unittest.TestCase):

    def setUp(self):
        self.tx = Transaction("Satheesh", "Chaitra", 10)
        self.newtx = Transaction("Chaitra", "Nala", 10)
        self.block = Block()
        self.block.add_transaction(self.tx)
        self.block.finalize()
        self.blockchain = []
        self.blockchain.append(self.block)

    def test_new_blockchain(self):
        newblock = Block(blockchain=self.blockchain)
        newtx = Transaction("Jeeva", "Satheesh", 2)
        newblock.add_transaction(newtx)
        newblock.finalize()
        self.blockchain.append(newblock)
        self.assertTrue(validatechain(self.blockchain))

    def test_invalid_blockchain(self):
        newblock = Block(blockchain=self.blockchain)
        newtx = Transaction("Jeeva", "Satheesh", 2)
        newblock.add_transaction(newtx)
        newblock.finalize()
        self.blockchain.append(newblock)
        thirdblock = Block(blockchain=self.blockchain)
        anothertx = Transaction("Jeeva", "Vinoth", 2)
        thirdblock.add_transaction(anothertx)
        thirdblock.finalize()
        #self.assertTrue(validatechain(self.blockchain))
        newblock.add_transaction(anothertx)
        self.blockchain[1] = newblock
        self.assertFalse(validatechain(self.blockchain))


if __name__ == '__main__':
    unittest.main()
