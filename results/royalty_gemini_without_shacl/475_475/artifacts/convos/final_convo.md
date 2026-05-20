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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Alexander, Crown Prince of Yugoslavia (Serbian: Александар Карађорђевић, Престолонаследник Југославије, romanized: Aleksandar Karađorđević, Prestolonaslednik Jugoslavije; born 17 July 1945), is the head of the House of Karađorđević, the former royal house of the defunct Kingdom of Yugoslavia and its predecessor the Kingdom of Serbia.
Alexander is the only child of King Peter II and Princess Alexandra of Greece and Denmark.
He held the position of crown prince in the Democratic Federal Yugoslavia for the first four-and-a-half months of his life, until the declaration of the Federal People's Republic of Yugoslavia later in November 1945, when the monarchy was abolished.
In public he claims the crowned royal title of "Alexander II Karadjordjevic" (Serbian: Александар II Карађорђевић, Aleksandar II Karađorđević) as a pretender to the throne.
Through his father, Alexander is a direct descendant of Queen Victoria, through his great-great-grandfather Prince Alfred, Duke of Saxe-Coburg and Gotha, Victoria's second eldest son.
Alexander is known for his support of constitutional monarchism and his humanitarian work.
He left Yugoslavia in April 1941 and arrived in London in June 1941.
Commenting on the event and what happened to his father, Crown Prince Alexander said, "He  was too straight.
On 29 November 1943, AVNOJ (formed by the Partisans) declared themselves the sovereign communist government of Yugoslavia and announced that they would take away all legal rights from the Royal government.
On 10 August 1945, less than a month after Alexander's birth, AVNOJ named the country Democratic Federal Yugoslavia.
On 29 November 1945, the country was declared a communist republic and changed its name to People's Federal Republic of Yugoslavia.
In 1947, all members of Alexander's family except for his granduncle Prince George were deprived of their Yugoslav citizenship and their property was confiscated.
As of 8 July 2015, the High Court in Belgrade found that decree 392, issued by the Presidency of the Presidium of the National Assembly on 3 August 1947, which deprived King Peter II and other members of the House of Karađorđević of their citizenship, was null and void from the moment of its adoption, in the parts pertaining to Crown Prince Alexander, and that all of its legal consequences are thus null and void.
Birth and childhood

Alexander was born in Suite 212 of Claridge's Hotel in Brook Street, Mayfair, London, on 17 July 1945.
The British Government is said to have temporarily ceded sovereignty over the suite in which the birth occurred to Yugoslavia so that the crown prince would be born on Yugoslav territory, though the story may be apocryphal, as there exists no documentary record of this.
Another part of the story says that a box of soil from the homeland was placed under the bed, so the Prince could be born on Yugoslav soil.
It is now Suite 214 and known as the 'Alexander Suite'.
He was the only child of King Peter II and Queen Alexandra of Yugoslavia.
His parents were relatively unable to take care of him due to their various health and financial problems, so Alexander was raised by his maternal grandmother, Princess Aspasia of Greece and Denmark.
Military service

Alexander graduated from the Royal Military Academy Sandhurst in 1966 and was commissioned as an officer into the British Army's 16th/5th The Queen's Royal Lancers regiment, rising to the rank of captain.
After leaving the army in 1972, Alexander, who speaks several languages, pursued a career in international business.
, he married Princess Maria da Gloria of Orléans-Braganza (b. 1946) from the Brazilian imperial family, at the parish church of St. Mary Magdalene.
They are double 4th cousins once removed as both are descendants of Prince Ferdinand of Saxe-Coburg and Gotha (1785–1851) and Princess Maria Antonia von Koháry (1797–1862), as well as of Pedro I, Emperor of Brazil and Archduchess Maria Leopoldina of Austria.
They have three sons: Peter (born 5 February 1980), and fraternal twins: Philip and Alexander (both born 15 January 1982).
Alexander and Maria da Gloria divorced on 19 February 1985.
Maria da Gloria married Ignacio de Medina, Duke of Segorbe (b. 1947), while Crown Prince Alexander married Katherine Clairy Batis, daughter of Robert Batis and Anna Dosti, civilly on 20 September 1985, and religiously the following day, at St. Sava Serbian Orthodox Church, Notting Hill, London.
Since their marriage, she is known as Crown Princess Katherine, as per the royal family's website.
On 16 December 2017, Alexander attended with his wife the state funeral of his first cousin once removed, King Michael of Romania in Bucharest, along with other heads of European royal families and invited guests.
On 19 September 2022, Crown Prince Alexander and his wife Katherine attended the state funeral of his godmother Queen Elizabeth II.
On 6 February 2024, following the news about King Charles' health, Alexander himself revealed that he had been treated for early stage prostate cancer in December 2023.
Return to Yugoslavia

Alexander first came to Yugoslavia in 1991.
He actively worked with the opposition to Slobodan Milošević and moved to Yugoslavia after Milošević had been deposed in 2000.
On 27 February 2001, the parliament of the Federal Republic of Yugoslavia (FRY) passed legislation conferring citizenship on members of the Karađorđević family.
The legislation may also have effectively annulled a decree stripping the family of its citizenship of the Socialist Federal Republic of Yugoslavia (SFRY) in 1947.
Belief in constitutional monarchy

Alexander is a proponent of re-creating a constitutional monarchy in Serbia and sees himself as the rightful king.
He believes that monarchy could give Serbia "stability, continuity and unity".
A number of political parties and organizations support a constitutional parliamentary monarchy in Serbia.
The assassinated former Serbian Prime Minister Zoran Đinđić was often seen in the company of the prince and his family, supporting their campaigns and projects, although his Democratic Party never publicly embraced monarchism.
Crown Prince Alexander has vowed to stay out of politics.
He and Princess Katherine spend considerable time engaging in humanitarian work.
The Crown Prince has, however, increasingly participated in public functions alongside the leaders of Serbia, the former Yugoslav republics and members of the diplomatic corps.
On 11 May 2006, he hosted a reception at the Royal Palace for delegates attending a summit on Serbia and Montenegro.
The reception was attended by the Governor of the National Bank of Serbia, as well as ambassadors and diplomats from Slovenia, Poland, Brazil, Japan, the United States, and Austria.
In addition, we in Serbia and Montenegro must take into account that whatever form we take within the European Union, we have only but one choice and that is to work for the common good of all member nations.
It is also central to take into account that stability in our region will be enhanced when Serbia is fully at peace with itself.
The Crown Prince raised the issue of a royal restoration in the immediate aftermath of the vote.
I strongly believe in a Constitutional Parliamentary Kingdom of Serbia.
Again, we need to be proud, a strong Serbia that is at peace with itself and with its neighbors.
Only if we have a form of governance close to the Serbian soul: the Kingdom of Serbia.
What is most important is the interest of Serbia.
I am ready to meet all our politicians; we have to work together for the common good of Serbia, and to be friends in the name of the future of our country.
I appeal for mature democratic debate in the interest of Serbia.
Serbia must have clear and realistic objectives.
The public also had reservations with Alexander's apparent lack of knowledge of the Serbian language.
On 27 July 2015, newspaper Blic published a poll "Da li Srbija treba da bude monarhija?" ("Should Serbia be a monarchy?"); 49.8% respondents expressed support in a reconstitution of monarchy, 44.6% were opposed and 5.5% were indifferent.
In 2017, an NGO, the Kingdom of Serbia Association, announced that in 2016, they had collected over 123,000 signatures of support for a referendum on Alexander being named king, short of the 150,000 needed to force a constitutional amendment.



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
  AssignClass (f605c437-233a-4c1c-bc09-d02262d5e660)
 Call ID: f605c437-233a-4c1c-bc09-d02262d5e660
  Args:
    type: :Man
    source: Alexander_Karađorđević
  AssignClass (242d3b8b-4df6-4097-8138-d8b7b0a8ec19)
 Call ID: 242d3b8b-4df6-4097-8138-d8b7b0a8ec19
  Args:
    type: :Man
    source: Peter_II
  AssignClass (f94416dc-8393-40c7-ba1c-a4d59dfb66d1)
 Call ID: f94416dc-8393-40c7-ba1c-a4d59dfb66d1
  Args:
    type: :Woman
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (fc8693d4-e370-40dc-9e5c-f5026583fca3)
 Call ID: fc8693d4-e370-40dc-9e5c-f5026583fca3
  Args:
    type: :Woman
    source: Aspasia_of_Greece_and_Denmark
  AssignClass (b30b4f47-bcca-4867-b4cf-e29c20c7243e)
 Call ID: b30b4f47-bcca-4867-b4cf-e29c20c7243e
  Args:
    type: :Woman
    source: Maria_da_Gloria_of_Orléans-Braganza
  AssignClass (d6f38ad5-3af8-444a-ab8e-a0cec1135bfc)
 Call ID: d6f38ad5-3af8-444a-ab8e-a0cec1135bfc
  Args:
    type: :Man
    source: Peter_Karađorđević
  AssignClass (83690ea6-adfb-464e-9cb5-68e17c0f820d)
 Call ID: 83690ea6-adfb-464e-9cb5-68e17c0f820d
  Args:
    type: :Man
    source: Philip_Karađorđević
  AssignClass (34951a65-efb7-42d7-a8a9-64473017548b)
 Call ID: 34951a65-efb7-42d7-a8a9-64473017548b
  Args:
    type: :Man
    source: Alexander_Karađorđević_Jr
  AssignClass (d4fbc9c3-d3a4-4ea1-acb0-cafbc9916e76)
 Call ID: d4fbc9c3-d3a4-4ea1-acb0-cafbc9916e76
  Args:
    type: :Man
    source: Ignacio_de_Medina
  AssignClass (a8e21287-084b-45d9-a92b-7df7a153b23c)
 Call ID: a8e21287-084b-45d9-a92b-7df7a153b23c
  Args:
    type: :Woman
    source: Katherine_Clairy_Batis
  AssignClass (894be456-f659-4f94-8e4e-e23ff3046943)
 Call ID: 894be456-f659-4f94-8e4e-e23ff3046943
  Args:
    type: :Man
    source: Robert_Batis
  AssignClass (5d1bfd11-a749-450a-8e38-cc7577fd1c84)
 Call ID: 5d1bfd11-a749-450a-8e38-cc7577fd1c84
  Args:
    type: :Woman
    source: Anna_Dosti
  AddTriple (4284466f-8287-4c38-bd74-33317fd6cb35)
 Call ID: 4284466f-8287-4c38-bd74-33317fd6cb35
  Args:
    target: Peter_II
    relation: :hasFather
    source: Alexander_Karađorđević
  AddTriple (d116da59-b1a8-482f-a0e4-e745e5389eb6)
 Call ID: d116da59-b1a8-482f-a0e4-e745e5389eb6
  Args:
    source: Alexander_Karađorđević
    relation: :hasMother
    target: Alexandra_of_Greece_and_Denmark
  AddTriple (96b46b0b-2e43-4b04-b41e-5f7ed8c6254c)
 Call ID: 96b46b0b-2e43-4b04-b41e-5f7ed8c6254c
  Args:
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasMother
    target: Aspasia_of_Greece_and_Denmark
  AddTriple (cdb672b5-c0ae-4738-95d6-41f2cb610e00)
 Call ID: cdb672b5-c0ae-4738-95d6-41f2cb610e00
  Args:
    target: Alexander_Karađorđević
    relation: :hasFather
    source: Peter_Karađorđević
  AddTriple (d2681dce-d3e2-49b4-adfd-826b9c5081d3)
 Call ID: d2681dce-d3e2-49b4-adfd-826b9c5081d3
  Args:
    target: Maria_da_Gloria_of_Orléans-Braganza
    relation: :hasMother
    source: Peter_Karađorđević
  AddTriple (6499e145-da66-4c36-889f-bb37904e2007)
 Call ID: 6499e145-da66-4c36-889f-bb37904e2007
  Args:
    source: Philip_Karađorđević
    target: Alexander_Karađorđević
    relation: :hasFather
  AddTriple (2d797ba9-e69c-46bc-96e6-c5e15c6ded1e)
 Call ID: 2d797ba9-e69c-46bc-96e6-c5e15c6ded1e
  Args:
    source: Philip_Karađorđević
    target: Maria_da_Gloria_of_Orléans-Braganza
    relation: :hasMother
  AddTriple (9606d6a0-46c5-4d9b-9670-b867aaf35a12)
 Call ID: 9606d6a0-46c5-4d9b-9670-b867aaf35a12
  Args:
    source: Alexander_Karađorđević_Jr
    relation: :hasFather
    target: Alexander_Karađorđević
  AddTriple (ba9588da-0ffb-4e71-a95c-01ffc573c433)
 Call ID: ba9588da-0ffb-4e71-a95c-01ffc573c433
  Args:
    relation: :hasMother
    target: Maria_da_Gloria_of_Orléans-Braganza
    source: Alexander_Karađorđević_Jr
  AddTriple (9406450f-39a7-449f-a5e9-268ea16b219f)
 Call ID: 9406450f-39a7-449f-a5e9-268ea16b219f
  Args:
    source: Katherine_Clairy_Batis
    target: Robert_Batis
    relation: :hasFather
  AddTriple (84eb0ea8-8432-4aa6-ba01-b96b98a0d94f)
 Call ID: 84eb0ea8-8432-4aa6-ba01-b96b98a0d94f
  Args:
    source: Katherine_Clairy_Batis
    target: Anna_Dosti
    relation: :hasMother
  AddLiteral (c5ef4bf6-d6c9-434e-bb25-2c7dbc368709)
 Call ID: c5ef4bf6-d6c9-434e-bb25-2c7dbc368709
  Args:
    relation: :hasBirthYear
    literal_value: 1945
    literal_type: xsd:integer
    source: Alexander_Karađorđević
  AddLiteral (d01bf976-c89b-4dd4-9b6d-fb7deecdc8a5)
 Call ID: d01bf976-c89b-4dd4-9b6d-fb7deecdc8a5
  Args:
    relation: :hasBirthYear
    literal_value: 1946
    source: Maria_da_Gloria_of_Orléans-Braganza
    literal_type: xsd:integer
  AddLiteral (033c683f-b00e-463e-90d3-5328484b0024)
 Call ID: 033c683f-b00e-463e-90d3-5328484b0024
  Args:
    literal_value: 1980
    relation: :hasBirthYear
    source: Peter_Karađorđević
    literal_type: xsd:integer
  AddLiteral (554ef470-d51f-415b-b03e-b406d3bf5ff5)
 Call ID: 554ef470-d51f-415b-b03e-b406d3bf5ff5
  Args:
    relation: :hasBirthYear
    literal_value: 1982
    literal_type: xsd:integer
    source: Philip_Karađorđević
  AddLiteral (822a40c5-ad01-4ebf-9706-2b888cc22514)
 Call ID: 822a40c5-ad01-4ebf-9706-2b888cc22514
  Args:
    literal_type: xsd:integer
    source: Alexander_Karađorđević_Jr
    literal_value: 1982
    relation: :hasBirthYear
  AddLiteral (41b3c6aa-fa42-41f4-9a7a-1544cd958b38)
 Call ID: 41b3c6aa-fa42-41f4-9a7a-1544cd958b38
  Args:
    literal_type: xsd:integer
    source: Ignacio_de_Medina
    relation: :hasBirthYear
    literal_value: 1947
  Finish (1a27e789-f1df-4d94-bb9d-6d339546e786)
 Call ID: 1a27e789-f1df-4d94-bb9d-6d339546e786
  Args: