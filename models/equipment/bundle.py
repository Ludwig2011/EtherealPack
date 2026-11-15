from Equipment import SpellBook
from Level import Equipment, SLOT_WEAPON, Tags
from mods.EtherealPack.models.spells.word_of_disjunction import WordOfDisjunction
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherStaff(Equipment):

	def on_init(self):
		self.name = "Äther Staff"
		self.slot = SLOT_WEAPON
		self.tags = [Ethereal]
		self.recipe = [(Ethereal, 1), (Tags.Any, 3)]

		self.tag_bonuses[Ethereal]['damage'] = 4
		self.tag_bonuses[Ethereal]['range'] = 3
		self.tag_bonuses[Ethereal]['num_targets'] = 3

class EmergenceStaff(Equipment):

	def on_init(self):
		self.name = "Staff of Emergence"
		self.slot = SLOT_WEAPON
		self.tags = [Ethereal]
		self.recipe = [(Ethereal, 2), (Tags.Conjuration, 2), (Tags.Any, 3)]

		self.tag_bonuses[Ethereal]['minion_damage'] = 4
		self.tag_bonuses[Ethereal]['minion_range'] = 3
		self.tag_bonuses[Ethereal]['num_summons'] = 2

class StabelizationStaff(Equipment):

	def on_init(self):
		self.name = "Staff of Stabelization"
		self.slot = SLOT_WEAPON
		self.tags = [Ethereal]
		self.recipe = [(Ethereal, 2), (Tags.Conjuration, 1), (Tags.Any, 3)]

		self.tag_bonuses_pct[Ethereal]['minion_health'] = 77
		self.tag_bonuses_pct[Ethereal]['minion_damage'] = 77

class SevenSeals(Equipment):

	def on_init(self):
		self.name = "~Abolish~ Seven Seals"
		self.tags = [Ethereal]
		self.recipe = [(Tags.Dark, 1), (Tags.Holy, 1), (Tags.Arcane, 1), (Tags.Chaos, 1), (Tags.Word, 1), (Tags.Translocation, 1), (Tags.Ritual, 1)]

        #TODO something more interesting? Disapear 7 enemies?
		self.tag_bonuses[Ethereal]['num_targets'] = 5
		self.tag_bonuses[Ethereal]['num_summons'] = 2


class BookOfDisjunction(SpellBook):

	def __init__(self):
		SpellBook.__init__(self, "Book of Disjunction", WordOfDisjunction)