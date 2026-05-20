================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Emilie Charlotte, Lady de Bathe (née Le Breton, formerly Langtry; 13 October 1853 – 12 February 1929), known as Lillie (or Lily) Langtry and nicknamed "The Jersey Lily", was a British socialite, stage actress and producer.
In 1881, Langtry became an actress and made her West End debut in the comedy She Stoops to Conquer, causing a sensation in London by becoming the first socialite to appear on stage.
She starred in many plays in both the United Kingdom and the United States, including The Lady of Lyons, and Shakespeare's As You Like It.
In later life she performed "dramatic sketches" in vaudeville.
From the mid-1890s until 1919, Langtry lived at Regal Lodge at Newmarket in Suffolk, England.
The Lillie Langtry Stakes horse race is named after her.
One of the most glamorous British women of her era, Langtry was the subject of widespread public and media interest.
Her acquaintances in London included Oscar Wilde, who encouraged Langtry to pursue acting.
She was known for her relationships with royal figures and noblemen, including Albert Edward, Prince of Wales (the future King Edward VII), Lord Shrewsbury, and Prince Louis of Battenberg.
Langtry refused to write her "real reminiscences", and remains somewhat of an enigmatic personality.
Life

Born in 1853 and known as Lillie from childhood, she was the daughter of the Very Reverend William Corbet Le Breton and his wife, Emilie Davis (née Martin), a recognised beauty.
Lillie's parents had eloped to Gretna Green in Scotland, and, in 1842, married at St Luke's Church, Chelsea, London.
Emilie Charlotte (Lillie) was born at the Old Rectory, St Saviour, on Jersey.
Lillie was the sixth of seven children and the only girl.
In an 1882-interview Lillie said: 'Yes, I was born and educated in Jersey, but it is not correct for you to say that I spent my bread-and-butter days there.
It would be more accurate to describe my girlhood as my " tomboy days," I think.'


Lillie's French governess was reputed to have been unable to manage her, so Lillie was educated by her brothers' tutor.
Life in London

On 9 March 1874, 20-year-old Lillie married 26-year-old Edward Langtry (1847–1897), a landowner from Ulster in the north of Ireland.
'Ned' Langtry was the widower of Jane Frances Price, whose sister, Elizabeth Ann Price, was the wife of Lillie's brother William.
Lillie and Edward held their wedding reception at The Royal Yacht Hotel in St Helier, Jersey.
Ned Langtry owned a large sailing yacht called Red Gauntlet, and Lillie insisted that he take her away from the Channel Islands.
In 1876 they rented an apartment in Eaton Place, Belgravia, London.
In 1877, Lillie's brother Clement married Alice, an illegitimate daughter of Viscount Ranelagh, their father's friend.
After meeting her in London, Ranelagh invited her to a reception attended by several notable artists at the home of Sir John and Lady Sebright on 29 April 1877.
Langtry was in mourning for her youngest brother, who had been killed in a riding accident, so in contrast to the elaborate clothes of most women in attendance, she wore a simple black dress (which was to become her trademark) and no jewellery.
Lady Sebrights' salon, where artistic and aristocratic audiences overlapped, was 'the ideal springboard' for Langtry.
In an 1882-interview, Langtry told how "y life in Jersey had been spent almost entirely in the open air, and as Mr Langtry was fond of yachting I became an expert yachtswoman and was very fond of all sorts of outdoor exercise, but I longed to see something more of the world."
After learning Lillie's identity, Miles "begged  to sit for a portrait."
The painting made then was purchased by Prince Leopold, and Lillie became famous and popular among the nobles of London and the royal family.
Another guest, Sir John Everett Millais, also a Jersey native, eventually painted her portrait, titling it A Jersey Lily after the Jersey lily flower (Amaryllis belladonna), a symbol of the country.
The portrait popularised Jersey Lily as Langtry's nickname, although Langtry was portrayed holding a Guernsey lily (Nerine sarniensis) in the painting, as no Jersey lilies were available.
A friend of Millais, Rupert Potter (father of Beatrix Potter), was a keen amateur photographer and took pictures of Lillie during her visit to Millais in Scotland in 1879.
She also sat for Sir Edward Poynter and is depicted in works by Sir Edward Burne-Jones.
In early 1878, the Langtrys moved to 17 Norfolk Street (now 19 Dunraven Street) off Park Lane to accommodate the growing demands of Lillie's society visitors.
Lillie Langtry arrived in the late 1870s, the heyday of 'the Professional Beauties'.
Margot Asquith later explained that Langtry's youth was the time 'of the great beauties.
London worshipped beauty like the Greeks'.
According to Asquith, Langtry became the centre of a social excitement excelling that around the other 'Beauties'. '
"The Jersey Lily" – as Mrs. Langtry was called – had Greek features, a transparent skin, arresting eyes, fair hair, and a firm white throat.
Langtry was beautiful in an 'unusual' way in vogue with pre-Raphaelite ideals: 'the column of a neck, the square jaw, the well-defined lips, the straight nose, the slate-blue eyes, the pale skin (she was nicknamed Lillie, she tells us, because of her lily-white complexion), even the hair loosely knotted in the nape off the neck'.
Her looks offered a good opportunity for painters: 'y sketches of Lillie during her first London season', wrote Miles twenty years later, 'earned far more than I've ever made on the largest commissions for my most expensive paintings.'
Winning Lillie even wider recognition were her photographic likenesses, a relatively new art.
Also many an aristocratic drawing room boasted a leather-bound, brass-locked album featuring the faces of the "Professional Beauties" of the season.
Asquith heard from her sister, Chartie Ribblesdale, about a ball at which "several fashionable ladies had stood upon their chairs to see Mrs. Langtry come into the room.
Among her adorers were the Prince of Wales, (King Edward) and the present Earl of Lonsdale."
Ribblesdale also remembered a story about Langtry and Lonsdale "paus at the railings in Rotten Row to talk to a man of her acquaintance.
I do not know what she could have said to him, but after a brief exchange of words, Lord Lonsdale jumped off his horse, sprang over the railings, and with clenched fists hit Mrs. Langtry's admirer in the face.
I may say that she had dewy, violet eyes, a complexion like a peach, and a mass of lovely hair drawn back in a soft knot at the nape of her classic head.
She was poor, and wore a dowdy black dress, but my stepfather lost his heart to her  The friends we had invited to meet the lovely Lily Langtry were as willingly magnetised by her unique personality as we were.
y own infatuation, for it was little less, for lovely Lily Langtry continued for many a day...
The average of good looks to-day is much higher, but there is none to equal Lily Langtry."
The royal biographer Theo Aronson has highlighted the importance of social changes that formed the backdrop of Langtry's success.
In the late 1870s, high society became less exclusive following the example of the Prince of Wales, who preferred the company of 'very rich men', regardless of whether they had an aristocratic lineage.
By the time Langtry was introduced, 'usiness acumen, beauty and, to a lesser extent, brains were becoming enough to get one accepted'.
This 'opening-up' partially explains the success of Langtry.
Her behaviour was in line with aristocratic expectations: 'her air, despite her vivacity and sensuality, was well-bred: she knew how to conduct herself in public'.
In 1878, Langtry attracted a lot of attention during the Ascot races, being 'at the height of her beauty and fame'.
According to Lady Augusta Fane's recollections, Langtry was made so popular by her 'naturalness' and charm; 'she had no affectations and no "make-up," either of face or mind; she was just herself, so no one could help loving her, with her gay, light-hearted nature'.
However, there was another reason why Langtry attracted so much attention in 1878: the Prince of Wales was often seen in public with her.
Royal mistress

On 24 May 1877, while his wife was staying in Athens with her brother, King George I of the Hellenes, Albert Edward, Prince of Wales, took supper with the Arctic explorer Sir Allen Young.
There, he met Edward and Lillie Langtry.
The 23-year-old Lillie had been discovered only a month earlier but had already taken London society by storm.
It was soon presumed that Langtry had become the mistress of the Prince of Wales, but no immediate scandal arose.
The Prince's wife, Alexandra of Denmark, accepted the situation and received her at parties in Marlborough House, the couple's London residence.
Jane Ridley has questioned the myth which Lillie Langtry created about herself, especially the role of the future Edward VII.
She critiques Langtry's narrative of herself as an innocent country girl to whom success just happened.
Ridley considers Langtry's entrance to London society to have been carefully planned, even if more successful than she could have hoped.
In an 1882 interview, Langtry herself said that 'y pedigree was good and my person in Jersey society being assured, it was not surprising that I should be well-received'.
Ridley also expressed doubts on the nature of Langtry's relationship with the Prince of Wales.
No letters from this time have survived, and many of the stories seem to be exaggerated or wrong.
For example, Langtry is alleged to have consummated her relationship with Prince Edward when his wife, Alexandra, refused to accompany him to a royal house party at Crichel in January 1878.
According to Ridley, Langtry published a false story about her presentation at court to Queen Victoria.
Langtry alleges that despite being presented towards the end of the evening, by when the Queen had usually retired, Victoria waited to see her.
Ridley concludes that this anecdote was made up by Langtry, as she alleged the presence of the Prince and Princess of Wales, who were in Paris at the time, probably on purpose to avoid embarrassing them by presenting the alleged mistress of Bertie.
In Ridley's view, Langtry invented stories implying that she was recognised as royal mistress.
Langtry Manor in Bournemouth, supposedly built for clandestine meetings between the Prince and Lillie at his orders, was in fact built for Emily Langton Langton.
Ridley could find no evidence about the exact nature of the relationship between Lillie Langtry and the Prince of Wales.
However, there is correspondence between the Prince's private secretary, Francis Knollys, and the Prince's solicitor, George Lewis, which suggests that Edward Langtry used George Lewis as a broker, offering his silence and cash in exchange for the Prince's love letters.
Lewis kept Knollys closely informed about the death of Edward Langtry in 1897.
The Prince of Wales, meanwhile, maintained a lifelong friendship with Lillie.
Whatever it exactly was, Lillie's liaison with the Prince lasted from late 1877 to June 1880.
The Shrewsbury scandal


In July 1879, Langtry began an affair with Lord Shrewsbury; in January 1880, they were planning to run away together.
In the autumn of 1879, Adolphus Rosenberg wrote in Town Talk of rumours that her husband would divorce her and cite, among others, the Prince of Wales as co-respondent.
The Prince of Wales instructed his solicitor George Lewis to sue.
In 1880, Langtry's reputation was tarnished by the Shrewsbury scandal, rumours of divorce, and a secret pregnancy.
Many people refused to receive her, and with the withdrawal of royal favour, creditors started demanding their money.
In October 1880, Langtry sold many of her possessions to meet her debts, allowing him to avoid a declaration of bankruptcy.
Lillie went abroad to give birth.
Afterwards, the Prince of Wales, staunch in friendship, procured an opening for her: he introduced her to the actor-manager Squire Bancroft, who controlled the Haymarket Theatre and the Prince of Wales’ theatres.
The Prince of Wales encouraged her by visiting the theatre while she was on stage and did everything in his power to help her.
Daughter

Lillie Langtry had a short affair with Prince Louis of Battenberg from March 1880.
Letters from Lillie to Arthur Clarence Jones (1854–1930) give the impression she also had an affair, or at least an intimate friendship, with Jones, a childhood friend of her brothers who lived on Jersey.
Arthur Jones was the brother of Lillie's sister-in-law; both were illegitimate children of Lord Ranelagh.
In June 1880, Lillie became pregnant.
Her husband was not the father; Edward Langtry had walked out after a libel case.
The obvious candidate was Prince Louis of Battenberg.
Jane Ridley compared the dates with the diary of the Prince of Wales: Prince Louis was staying at Marlborough House on June 27, the likely conception date.
Lillie led Prince Louis to believe he was the father of her child.
She was lent £2000 by the Prince of Wales to pay her debts.
At the same time, Edward Langtry, who often visited unannounced, was prevented from seeing her.
Edward was constantly occupied with invitations to shoot or fish.
The concern was that if he discovered that Lillie was pregnant by another man, he might sue for divorce, dragging the Prince of Wales into the law courts.
Lillie spent the summer holiday in Jersey.
One Friday in October, by now four months pregnant, she visited London briefly and saw the Prince of Wales.
On 17 October, the Prince met with his doctor, Oscar Clayton, and saw Louis Battenberg.
The same day, Louis departed on a two-year voyage round the world on the aptly named warship HMS Inconstant.
Lillie was spirited away to France.
The moment it became clear that Lillie was pregnant, Battenberg's parents acted promptly.
An aide-de-camp was sent from the German Jugenheim to arrange a financial settlement.
Louis was told that there could be no question of marriage.
Suddenly, the Admiralty found an appointment for Louis Mountbatten on The Inconstant.
The passionate affair was ended before the child was born and with Louis Battenberg out of the way.
The discovery in 1978 of Langtry's letters to Arthur Jones and publication of quotations from them by Laura Beatty in 1999 support the idea that Jones was the father of Langtry's daughter.
Prince Louis' son, Earl Mountbatten of Burma, however, had always maintained that his father was the father of Jeanne Marie.
She was asked sharply by her mother, 'Who would you prefer to have as a father, a penniless drunken Irishman or a Royal Prince and the most handsome of all naval officers?'


Descendants

In 1902, Jeanne Marie Langtry married the Scottish politician Sir Ian Malcolm at St Margaret's, Westminster.
Jeanne Marie died in 1964.
Her daughter Mary Malcolm was one of the first two female announcers on the BBC Television Service (now BBC One) from 1948 to 1956.
The Guardian published an obituary mentioning Mary Malcolm was the granddaughter of King Edward VII.
It was rectified: 'This obituary of the postwar BBC television announcer Mary Malcolm said her mother, Jeanne-Marie, was the daughter of Lillie Langtry and Edward VII, the only one of his illegitimate children he acknowledged.
Although Langtry was Edward VII's mistress, the father of her daughter was acknowledged to be Prince Louis of Battenberg, grandfather of Prince Philip.'
The Times published an obituary mentioning Jeanne Marie Langtry had grown-up believing she was the daughter of Edward VII: 'Malcolm had an aristocratic pedigree.
She was a granddaughter of Lillie Langtry, actress, beauty and mistress of the Prince of Wales, later Edward VII.
Her mother, Jeanne Marie, was conceived and born out of wedlock, and  Malcolm grew up believing that she was the daughter of a king.
Only later did she learn that her father was Prince Louis of Battenberg, whose legitimate children included the future Earl Mountbatten of Burma.'
The prestigious Oxford Dictionary of National Biography also names Louis Mountbatten as grandfather of Mary Malcolm. '
Her mother was frequently assumed to be the illegitimate offspring of Edward VII (when prince of Wales).
Jeanne-Marie's father was (or at least was acknowledged to be)
German-born Prince Louis of Battenberg.
He anglicized his name on settling in Britain and it was his grandson Philip Mountbatten who in due course would marry into royalty and become duke of Edinburgh and consort of Queen Elizabeth II.'
The Daily Telegraph did mention Lillie Langtry, but not the assumed (grand)father.
Jeanne Marie's second son, Victor Neill Malcolm, married English actress Ann Todd.
Victor Malcolm remarried in 1942, to an American, Mary Ellery Channing.
Acting career and manager

In 1881, Langtry was in need of money.
Her close friend Oscar Wilde suggested she try the stage, and Langtry embarked upon a theatrical career.
It was a comedy two-hander called A Fair Encounter, with Henrietta Labouchère taking the other role and coaching Langtry in her acting.
Following favourable reviews of this first attempt at the stage, and with further coaching, Langtry made her debut before the London public, playing Kate Hardcastle in She Stoops to Conquer at the West End's Haymarket Theatre in December 1881.
Although her affair with the Prince of Wales was over, he supported her new venture by attending several of her performances and helping attract an audience.
Early in 1882, Langtry quit the production at the Haymarket and started her own company, touring the UK with various plays.
American impresario Henry Abbey arranged a tour in the United States for Langtry.
Before leaving New York, she had an acrimonious break with Henrietta Labouchère over Langtry's relationship with Frederick Gebhard, a wealthy young American.
While the critics generally condemned her interpretations of roles such as Pauline in The Lady of Lyons or Rosalind in As You Like It, the public loved her.
After her return from New York in 1883, Langtry registered at the Conservatoire in Paris for six weeks' intensive training to improve her acting technique.
The New York Times thought that Mrs Langtry's jewels were worth $100,000; her attire was so wonderful, so dazzling, so recklessly inappropriate -as
From 1900 to 1903, with financial support from Edgar Israel Cohen, Langtry became the lessee and manager of London's Imperial Theatre.
In a film released in 1913 directed by Edwin S. Porter, Langtry starred opposite Sidney Mason in the role of Mrs Norton in His Neighbor's Wife in what would be her only film appearance.
Thoroughbred racing

For nearly a decade, from 1882 to 1891, Langtry had a relationship with an American, Frederick Gebhard, described as a young clubman, sportsman, horse owner, and admirer of feminine beauty, both on and off the stage.
With Gebhard, Langtry became involved in horse racing.
On 13 August 1888, Langtry and Gebhard travelled in her private carriage attached to an Erie Railroad express train bound for Chicago.
One person died in the fire, along with Gebhard's champion runner Eole and 14 racehorses belonging to him and Langtry.
He was named for St Saviour's Church in Jersey, where Langtry's father had been rector and where she chose to be buried.
Despite speculation, Langtry and Gebhard never married.
In 1905 he married Marie Wilson; he died in 1910.
In 1889, Langtry met "an eccentric young bachelor, with vast estates in Scotland, a large breeding stud, a racing stable, and more money than he knew what to do with": this was George Alexander Baird or Squire Abington, as he came to be known.
Langtry and Baird met at a racecourse when he gave her a betting tip and the stake money to place on the horse.
The horse won several races under Langtry's colours; he was registered to "Mr Jersey" (women were excluded from registering horses at this time).
Langtry became involved in a relationship with Baird, from 1891 until his death in March 1893.
When Baird died, Langtry purchased two of his horses, Lady Rosebery and Studley Royal, at the estate dispersal sale.
Langtry found mentors in Captain James Octavius Machell and Joe Thompson, who provided guidance on all matters related to the turf.
In 1899, James Machell sold his Newmarket stables to Colonel Harry Leslie Blundell McCalmont, a wealthy racehorse owner, who was Langtry's brother-in-law, having married Hugo de Bathe's sister Winifred in 1897.
He was also related to Langtry's first husband, Edward, whose ship-owning grandfather George had married into the County Antrim Callwell family, being related in marriage to the McCalmonts.
Langtry later had a second Cesarewitch winner with Yentoi, and a third place with Raytoi.
Other trainers used by Langtry were Jack Robinson, who trained at Foxhill in Wiltshire, and a very young Fred Darling, whose first big success was Yentoi's 1908 Cesarewitch.
Langtry owned a stud at Gazely, Newmarket.
Langtry sold Regal Lodge and all her horse-racing interests in 1919 before she moved to Monaco.
Regal Lodge had been her home for twenty-three years and received many celebrated guests, notably the Prince of Wales.
In honour of her contributions to thoroughbred racing, since 2014 the Glorious Goodwood meeting has held the Group 2 Lillie Langtry Stakes.
William Ewart Gladstone – Prime Minister

During her stage career, Lillie Langtry became friendly with William Ewart Gladstone (1809–1898), who was the Prime Minister on four occasions during the reign of Queen Victoria.
In her memoirs, Langtry says that she first met Gladstone when she was posing for her portrait at Millais' studio.
However, this was probably also a make-belief by Lillie Langtry herself.
They are also quite cynical about Lillie's motives.
Lillie Langtry in The Days I Knew:
His comprehensive mind and sweet nature grasped the difficult task that lay before me, the widely different orbit in which my life would henceforth move, and he knew how adrift I felt.
Among his many excellent admonitions I remember, and shall always remember, this sound piece of advice.
However, it was not Gladstone who sought Lillie out; the approach came from Lillie.
Abraham Hayward, an influential journalist, wrote Gladstone a letter, dated 8 January 1882: 'Mrs Langtry, who is an enthusiastic admirer of yours, told me this afternoon that she should be feel highly flattered if you would call on her, and I tell you this, although I fear you have other more pressing overtures just at present.
Her address is 18 Albert Mansions, Victoria Street, and she is generally at home about six.'


The published diaries of Gladstone show there were indeed contacts between Lillie Langtry and one of the most important British statesmen.
Rumours were not surprising given Lillie's reputation and the gossip about Gladstone's nocturnal activities which circulated in London clubs.
Gladstone was in the habit of wanting to "rescue" prostitutes by trying to convince them it was best not to live in sin and to find a decent job.
On 16 February 1885 he wrote: 'Saw Mrs Langtry: probably for the last time.'
Gladstone's private secretary was worried about the contacts between Lillie Langtry and Gladstone: he was afraid she tried to make social capital out of their contacts.
'Last week Mr. G. received an invitation to a Sunday "at home" from Mrs Langtry.
Gladstone presented Lillie Langry a copy of his favourite book, Sister Dora – a biography of a high-born woman who worked as a nurse among the poor.
It seems Lillie Langtry had become by April 1882 a social outcast, with two important men who tried to help her: the Prince of Wales and the Prime Minister.
However, the much later published diaries of Gladstone himself show Hamilton had little to fear: there were little personal contacts with Lillie Langtry.
Gladstone wrote her exactly one letter in the short period after Lillie tried to (re)make contact with him while Gladstone didn't know well how to deal with the situation.
In it, he claimed that Gladstone had numerous extramarital affairs, including one with Langtry.
During the trial, a telegram, sent by Langtry from Monte Carlo, was read out in court saying, "I strongly repudiate the slanderous accusations of Peter Wright."
American citizenship and divorce

In 1888, Langtry became a property owner in the United States when she and Frederick Gebhard purchased adjoining ranches in Lake County, California.
Bearing the Langtry Farms name, the winery and vineyard are still in operation in Middletown, California.
During her travels in the United States, Langtry became an American citizen and on 13 May 1897, divorced her husband Edward in Lakeport, California.
In June of that year Edward Langtry issued a statement giving his side of the story, which was published in the New York Journal.
Edward died a few months later in Chester Asylum, after being found by police in a demented condition at Crewe railway station.
A letter of condolence later written by Langtry to another widow reads in part, "I too have lost a husband, but alas!
"


Langtry continued to have involvement with her husband's Irish properties after his death.
Hugo Gerald de Bathe

After the divorce from her husband, Langtry was linked in the popular press to Prince Paul Esterhazy , an Austro-Hungarian diplomat.
The wedding between Langtry and de Bathe took place in St Saviour's Church, Jersey, on 27 July 1899, with her daughter Jeanne Marie Langtry being the only other person present, apart from the officials.
This was the same day that Langtry's horse Merman won the Goodwood Cup.
In 1907, General de Bathe, Hugo's father, died; Hugo thus became the 5th Baronet, and Langtry became Lady de Bathe.
One of the houses on the site is named Langtry and another Hardy.
Final days

During her final years, Langtry, as Lady de Bathe, resided in Monaco whilst her husband, Sir Hugo de Bathe, lived in Vence, Alpes Maritimes.
Langtry's closest companion during her time in Monaco was her friend Mathilde Marie Peat.
Peat was at Langtry's side during the final days of her life as she was dying of pneumonia in Monte Carlo.
Langtry left Peat £10,000, the Monaco property known as Villa le Lys, clothes, and her motor car.
Langtry died in Monaco at dawn on 12 February 1929.
The death of the famous Lillie Langtry made headlines in British newspapers.
The Daily Mail remembered Lillie Langtry as one of the most famous beauties of the closed century.
The Daily Telegraph published both a news article and an obituary full of memories of a contemporary of Lillie Langtry who had known her in society years and had followed her acting career.
'Never a real actress' was the verdict, but Lillie Langtry had made the wise and honourable decision to use her celebrity to find a career and her living in her own way and by her own resources instead of becoming dependent on offers of aristocratic male friends after her separation from her husband.
The Times published on three different pages a news alert from the correspondent in Paris, a photograph and an obituary.
In the obituary the newspaper looked  back at the start and the development of Langtry's career.
‘The audience, which included the Prince and Princess of Wales, and representatives of eminence in fashion, art, and literature, received Mrs. Langtry very quietly, but the debutante soon overcame the feeling of prejudice....
Mrs. Langtry became so popular in America that she paid many visits to that country, her last being in 1915.
The Manchester Guardian remembered Lillie Langtry mainly as a "reigning beauty".
'The London of the eighties and nineties, when the "Jersey Lily," whose death is announced, had her heyday, seems even more remote than the passage of years warrants.
To a generation whose manifold interests in life have enormously increased in comparison with their fathers' it seems incredible that barely a generation ago crowds should have assembled in thousands to stare at or cheer a "reigning beauty."
Yet Mrs. Langtry, though the most famous of her kind, was no exception as a social institution....
But it can at least admire the "Jersey Lily" for one fact in her curious career – that when hard times came she turned to hard work for the theatre.
That work was seldom artistically notable but it revealed a force of character on which those who reckoned her by looks alone had hardly counted.'
Langtry was not perhaps a great actress, but her beauty carried everything before it.
It was one of her plaints that "to-day women are becoming so standardised in figure and dress that they all seem to look like each other."
In the United States the death of Lillie Langtry was front page news for the New York Times.
The Washington Post reported the news on page 13, but still in a prominent way: a friend of King of Edward VII and one of the most popular women of stage had died.
Bequests

Immediately after her death, the Daily Mail published exclusive news: ‘The Daily Mail understands that Lady de Bathe, (Mrs. Langtry, " the Jersey Lily "), who died at Monte Carlo on February 12, has made a number of personal bequests in her will.
To her daughter, Lady (Ian) Malcolm, Lady de Bathe left the family old silver from Jersey.
To the two daughters of Lady (Ian) Malcolm she left £5,000 each.
She was accompanied by Lady Malcolm and the solicitor to the estate.’
In her will, Langtry left £2,000 to a young man of whom she had become fond in later life, named Charles Louis D'Albani; the son of a Newmarket solicitor, he was born in about 1891.
Cultural influence and portrayals

One of the most glamorous British women of her era, Langtry used her high public profile to endorse commercial products such as cosmetics and soap—an early example of celebrity endorsement.
The aesthetic movement in England became directly involved in advertising, and Pears (under advertising pioneer Thomas J. Barratt) recruited Langtry—who had been painted by aesthete artists—to promote their products, which included putting her "signature" on the advertisements.
In the 1944 Universal film The Scarlet Claw, Lillian Gentry, the first murder victim, wife of Lord William Penrose and former actress, is an oblique reference to Langtry.
Langtry has been portrayed in two films.
Lilian Bond played her in The Westerner (1940), and Ava Gardner in The Life and Times of Judge Roy Bean (1972).
In 1978, Langtry's story was dramatised by London Weekend Television and produced as Lillie, starring Francesca Annis in the title role (Annis received the British Academy Television Award for Best Actress).
Annis previously played Langtry in two episodes of ATV's Edward the Seventh.
Langtry is a featured character in the fictional The Flashman Papers novels of George MacDonald Fraser, in which she is noted as a former lover of arch-cad Harry Flashman, who, nonetheless, describes her as one of his few true loves.
Langtry is suggested as an inspiration for Irene Adler, a character in the Sherlock Holmes fiction of Sir Arthur Conan Doyle.
Langtry is used as a touchstone for old-fashioned manners in Preston Sturges's comedy The Lady Eve (1941), in a scene where a corpulent woman drops a handkerchief on the floor and the hero ignores it.
That hasn't been used since Lillie Langtry ...
"


Lillie Langtry is the inspiration for The Who's 1967 hit single "Pictures of Lily", as mentioned in Pete Townshend's 2012 memoir Who I Am.
Dixie Carter portrays Langtry as a "songbird" and Brady Hawkes' love interest in Kenny Rogers' 1994 Gambler V: Playing for Keeps, the last of the Gambler series for CBS that started in 1980.
Langtry is depicted as a singer, not an actress, and Dixie Carter's costuming appears closer to Mae West than anything Langtry ever wore.
In The Simpsons 1994 episode "Burns' Heir", the auditions are held in the Lillie Langtry Theater on Burns' estate.
Langtry is a featured character in the play Sherlock Holmes and the Case of the Jersey Lily by Katie Forgette.
In this work, she is blackmailed over her past relationship with the Prince of Wales, with intimate letters as proof.
Places connected with Lillie Langtry

Residences and historical namesakes

When first married (1874), Edward and Lillie Langtry had a property called Cliffe Lodge in Southampton, Hampshire.
In 1876 they rented an apartment in Eaton Place, Belgravia, London.
Langtry lived at 21 Pont Street, London, from 1890 to 1897, and had with her eight servants at the 1891 census.
A short walk from Pont Street was a house at number 2 Cadogan Place where she lived in 1899.
Langtry's London address from 1916 until at least 1920 was Cornwall Lodge, Allsop Place, Regent's Park.
A letter sold at auction in 2014 from Langtry to Dr. Harvey dated 1918 is also headed with this address.
Langtry was a cousin of local politician Philip Le Breton, pioneer for the preservation of Hampstead Heath, whose wife was Anna Letitia Aikin.
There are two bars in New York City devoted to the memory of Lillie Langtry, operating under the title Lillie's Victorian Establishment.
Judge Roy Bean named the saloon, in Pecos, Texas, The Jersey Lily, which also served as the judge's courthouse, for her, in Langtry, Texas (named after the unrelated engineer George Langtry).
Spurious associations

Bournemouth

In 1938 the new owners of the Red House at 26 Derby Road, Bournemouth, which had been built in 1877 by the widowed women's rights campaigner and temperance activist Emily Langton Langton, converted the large house into a hotel, the Manor Heath Hotel, and advertised it as having been built for Lillie Langtry by the Prince of Wales, believing that the inscription 'E.L.L. 1877' in one of the rooms related to Lillie Langtry.
A plaque was later placed on the hotel by Bournemouth Council repeating the assertion, and in the late 1970s the hotel was renamed Langtry Manor.
However, despite the hotel's claims and local legend, no actual association between Langtry and the house ever existed and the Prince never visited it.
South Hampstead

On 2 April 1965 the Evening Standard reported an interview with Electra Yaras (born c. 1922), leaseholder and resident of Leighton House, 103 Alexandra Road, South Hampstead, who claimed in the interview that Langtry had lived in the house and regularly entertained the Prince of Wales there.
Yaras claimed that she herself had been visited in the house several times by Langtry's ghost.
On 11 April 1971 The Hampstead News said that the house had been built for Langtry by Lord Leighton.
Lengthy research into local records by Dick Weindling and Marianne Colloms revealed no connection whatever with Langtry.
The persistence of the myth, propounded in a time when stories about the royal family were easy to publicise and received no critical or substantiating research, resulted in Langtry's name still being in use in some place names and locales in the South Hampstead area.
These include Langtry Road off Kilburn Priory; Langtry Walk in the Alexandra Road Estate; and the Lillie Langtry pub at 121 Abbey Road (defunct since late 2022), built in 1969 to replace The Princess of Wales hotel, and briefly called The Cricketers from 2007 to 2011.
The mythologising also includes The Lillie Langtry pub at 19 Lillie Road in Fulham—the road actually took its name from local landowner John Scott Lillie.
Steam yacht White Ladye

Langtry owned a luxury steam auxiliary yacht called White Ladye from 1891 to 1897.
In 1893, Ogden Goelet leased the vessel from Langtry and used it until his death in 1897.
Langtry put the White Ladye up for auction in November 1897 at the Mart, Tokenhouse Yard, London.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e5fc8239-3b47-4e89-aff4-7201479518e2)
 Call ID: e5fc8239-3b47-4e89-aff4-7201479518e2
  Args:
    source: Emilie_Charlotte_Le_Breton
    type: :Woman
  AssignClass (23327312-b7a3-43d2-aae1-c695d253093c)
 Call ID: 23327312-b7a3-43d2-aae1-c695d253093c
  Args:
    source: Emilie_Charlotte_Le_Breton
    type: :Person
  AddLiteral (98eac36f-4e11-4867-b352-93c6cc913eaf)
 Call ID: 98eac36f-4e11-4867-b352-93c6cc913eaf
  Args:
    literal_value: Lillie Langtry
    relation: :knownAs
    literal_type: xsd:string
    source: Emilie_Charlotte_Le_Breton
  AddLiteral (5a8ba157-b1a8-4748-996f-ebaeeae2bfb2)
 Call ID: 5a8ba157-b1a8-4748-996f-ebaeeae2bfb2
  Args:
    relation: :alsoKnownAs
    literal_value: Lily Langtry
    literal_type: xsd:string
    source: Emilie_Charlotte_Le_Breton
  AddLiteral (80821b0d-6032-4fa4-b9b7-8d37b9f77a37)
 Call ID: 80821b0d-6032-4fa4-b9b7-8d37b9f77a37
  Args:
    source: Emilie_Charlotte_Le_Breton
    literal_type: xsd:string
    literal_value: The Jersey Lily
    relation: :alsoKnownAs
  AddLiteral (5962f951-73d5-4d7a-8377-b6c44a99d61b)
 Call ID: 5962f951-73d5-4d7a-8377-b6c44a99d61b
  Args:
    literal_value: 1853
    relation: :hasBirthYear
    source: Emilie_Charlotte_Le_Breton
    literal_type: xsd:integer
  AddLiteral (7d91a5c5-fb7f-42fd-89a1-38b9a51ce59e)
 Call ID: 7d91a5c5-fb7f-42fd-89a1-38b9a51ce59e
  Args:
    source: Emilie_Charlotte_Le_Breton
    literal_type: xsd:integer
    literal_value: 1929
    relation: :hasDeathYear
  AssignClass (55640f2a-6a6e-4a36-b65d-aa5ccd9027dd)
 Call ID: 55640f2a-6a6e-4a36-b65d-aa5ccd9027dd
  Args:
    source: William_Corbet_Le_Breton
    type: :Man
  AssignClass (4a0b4b01-91cd-45f0-93b6-ec388c0ad68d)
 Call ID: 4a0b4b01-91cd-45f0-93b6-ec388c0ad68d
  Args:
    source: William_Corbet_Le_Breton
    type: :Person
  AssignClass (11703a0e-34be-4e26-9e2b-696b96ea0396)
 Call ID: 11703a0e-34be-4e26-9e2b-696b96ea0396
  Args:
    source: Emilie_Davis_Martin
    type: :Woman
  AssignClass (7b8e8f5f-a39c-41d2-a808-f003624ab9f7)
 Call ID: 7b8e8f5f-a39c-41d2-a808-f003624ab9f7
  Args:
    type: :Person
    source: Emilie_Davis_Martin
  AddTriple (d71f4312-f569-4d55-bf9b-e33ec0c86f61)
 Call ID: d71f4312-f569-4d55-bf9b-e33ec0c86f61
  Args:
    relation: :hasFather
    target: William_Corbet_Le_Breton
    source: Emilie_Charlotte_Le_Breton
  AddTriple (24218e00-9421-40c9-b593-32dfe2bed11b)
 Call ID: 24218e00-9421-40c9-b593-32dfe2bed11b
  Args:
    source: Emilie_Charlotte_Le_Breton
    target: Emilie_Davis_Martin
    relation: :hasMother
  AssignClass (436140c4-2067-4701-8be0-12595aa92059)
 Call ID: 436140c4-2067-4701-8be0-12595aa92059
  Args:
    source: Edward_Langtry
    type: :Man
  AssignClass (0dbb2579-5db3-474c-ad3b-872c8f90873a)
 Call ID: 0dbb2579-5db3-474c-ad3b-872c8f90873a
  Args:
    type: :Person
    source: Edward_Langtry
  AddLiteral (b4d09260-3b43-424a-817c-b17d4f98b52a)
 Call ID: b4d09260-3b43-424a-817c-b17d4f98b52a
  Args:
    relation: :hasMarriageYear
    literal_value: 1874
    source: Emilie_Charlotte_Le_Breton
    literal_type: xsd:integer
  AddTriple (b6b45330-980e-4d80-b3c1-7c376a743d9b)
 Call ID: b6b45330-980e-4d80-b3c1-7c376a743d9b
  Args:
    target: Edward_Langtry
    source: Emilie_Charlotte_Le_Breton
    relation: :hasRelation
  AssignClass (1700366c-af6b-4a9d-8734-fd45f5c2b7e3)
 Call ID: 1700366c-af6b-4a9d-8734-fd45f5c2b7e3
  Args:
    source: Jeanne_Marie_Langtry
    type: :Woman
  AssignClass (22b4ed64-e92b-47b4-adc1-4b452398ce02)
 Call ID: 22b4ed64-e92b-47b4-adc1-4b452398ce02
  Args:
    type: :Person
    source: Jeanne_Marie_Langtry
  AddTriple (61e30e89-3df8-458c-8d99-5f7bde7d2caf)
 Call ID: 61e30e89-3df8-458c-8d99-5f7bde7d2caf
  Args:
    relation: :isMotherOf
    target: Jeanne_Marie_Langtry
    source: Emilie_Charlotte_Le_Breton
  AssignClass (736f3692-198a-47ca-bb5f-2e7b9b52b33e)
 Call ID: 736f3692-198a-47ca-bb5f-2e7b9b52b33e
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (f899a060-b238-42e0-b9ef-339619166669)
 Call ID: f899a060-b238-42e0-b9ef-339619166669
  Args:
    type: :Person
    source: Prince_Louis_of_Battenberg
  AddTriple (aea9d71c-eabb-4ec4-9a52-0a5636ca0f94)
 Call ID: aea9d71c-eabb-4ec4-9a52-0a5636ca0f94
  Args:
    relation: :hasFather
    source: Jeanne_Marie_Langtry
    target: Prince_Louis_of_Battenberg
  AssignClass (0365a0b6-6591-4555-b848-c8f826299552)
 Call ID: 0365a0b6-6591-4555-b848-c8f826299552
  Args:
    type: :Man
    source: Hugo_Gerald_de_Bathe
  AssignClass (c6ae46b9-00f8-4064-a8c7-ed7480b15d96)
 Call ID: c6ae46b9-00f8-4064-a8c7-ed7480b15d96
  Args:
    type: :Person
    source: Hugo_Gerald_de_Bathe
  AddLiteral (db6a10e4-d562-4f59-9872-1a6737198906)
 Call ID: db6a10e4-d562-4f59-9872-1a6737198906
  Args:
    literal_value: 1899
    relation: :hasMarriageYear
    source: Emilie_Charlotte_Le_Breton
    literal_type: xsd:integer
  AddTriple (d486b031-3b5b-47b9-8fdb-017a7524f9cc)
 Call ID: d486b031-3b5b-47b9-8fdb-017a7524f9cc
  Args:
    relation: :hasRelation
    source: Emilie_Charlotte_Le_Breton
    target: Hugo_Gerald_de_Bathe
  Finish (0d1a3c8f-2bdb-4865-9c63-d8a13644a688)
 Call ID: 0d1a3c8f-2bdb-4865-9c63-d8a13644a688
  Args: