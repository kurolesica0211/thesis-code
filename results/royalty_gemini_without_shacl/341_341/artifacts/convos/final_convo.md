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
Ernest Augustus (Ernest Augustus Christian George; German: Ernst August Christian Georg; 17 November 1887 – 30 January 1953) was Duke of Brunswick from 2 November 1913 to 8 November 1918.
Early life

Ernest Augustus was born at Penzing near Vienna, the sixth and youngest child of former Crown Prince Ernest Augustus of Hanover and his wife, Princess Thyra of Denmark.
His great-grandfather, Prince Ernest Augustus, Duke of Cumberland, the fifth son of George III of the United Kingdom, became king of Hanover in 1837 because Salic Law barred Victoria, Queen of the United Kingdom, from inheriting the Hanoverian throne.
His father succeeded as pretender to the Hanoverian throne and as Duke of Cumberland and Teviotdale in the peerage of Great Britain in 1878.
The younger Ernest Augustus became heir apparent to the dukedom of Cumberland and to the Hanoverian claim upon the deaths of his two elder brothers, George and Christian.
In 1884, his paternal great-granduncle the reigning Duke of Brunswick (a male line descendant of Henry, the older brother of William, his male line ancestor) died.
Since the younger branch of the House of Welf ended with him, under house rules it would have passed to the Duke of Cumberland, who immediately claimed the throne.
However, the Imperial Chancellor, Otto von Bismarck, managed to get the Federal Council (Bundesrat) of the German Empire to rule that the Duke of Cumberland would disturb the peace of the empire if he ascended the throne of Brunswick.
Bismarck did this because the duke had never formally renounced his claims to the kingdom of Hanover, which had been annexed to Prussia in 1866 following the end of the Austro-Prussian War (Hanover had sided with losing Austria).
Instead, Prince Albrecht of Prussia became the regent of Brunswick.
After Prince Albrecht's death in 1906, the duke offered that he and his elder son, Prince George, would renounce their claims to the Duchy of Brunswick in order to allow Ernest Augustus, his only other surviving son, to take possession of the Duchy, but this option was rejected by the Bundesrat and the regency continued, this time under Duke Johann Albrecht of Mecklenburg-Schwerin, who had previously acted as regent for his nephew in Mecklenburg.
Marriage and accession to the duchy of Brunswick

When Ernest Augustus's older brother George died in an automobile accident on 20 May 1912, the German Emperor, Wilhelm II, sent a message of condolence to the Duke of Cumberland.
In response to this friendly gesture, the Duke sent his only surviving son, Ernest Augustus, to Berlin to thank the Emperor for his message.
Ernest Augustus and Wilhelm II were third cousins through George III of the United Kingdom.
In Berlin, Ernest Augustus met and fell in love with the emperor's only daughter, Princess Victoria Louise of Prussia.
On 24 May 1913, Ernest Augustus and Victoria Louise, third cousins once removed through descent from George III's sons King Ernest Augustus of Hanover and Edward, Duke of Kent, were married to each other.
This marriage ended the decades-long rift between the Houses of Hohenzollern and Hanover.
The wedding of Prince Ernest Augustus and Princess Victoria Louise was also the last great gathering of European sovereigns before the outbreak of the Great War, as recalled by Constantine II of Greece, a grandson of the married couple, in 2003.
In addition to the German Emperor and Empress and the Duke and Duchess of Cumberland, King George V and Queen Mary of the United Kingdom and Tsar Nicholas II attended.
Upon the announcement of his betrothal to Princess Victoria Louise in February 1913, Ernest Augustus swore allegiance to the German Empire and accepted a commission as a cavalry captain and company commander in the Zieten–Hussars, a Prussian Army regiment in which his grandfather (George V) and great-grandfather (Ernest Augustus) had been colonels.
On 27 October 1913, the Duke of Cumberland formally renounced his claims to the duchy of Brunswick in favor of his surviving son.
The following day, the Federal Council voted to allow Ernest Augustus to become the reigning Duke of Brunswick.
The new Duke of Brunswick formally took possession of his duchy on 1 November.
The new duke and duchess of Brunswick moved into Brunswick Palace in the capital of Brunswick and began their family with the birth of their eldest son, Prince Ernest Augustus, less than a year after their wedding.
During the First World War, Ernest Augustus rose to the rank of major-general.
Abdication and later life

In 1917, the British dukedom of Ernest Augustus's father, and his own title as a Prince of the United Kingdom of Great Britain and Ireland, were removed by the Titles Deprivation Act 1917, which took effect in 1919, as a result of the Duke's service in the German army during the war.
On 8 November 1918, Ernest Augustus was forced to abdicate his throne, as were all the other German kings, grand dukes, dukes, and princes during the German Revolution of 1918–1919.
Thus, when his father died in 1923, Ernest Augustus did not succeed to his father's title of Duke of Cumberland.
For the next thirty years, Ernest Augustus remained as head of the House of Hanover, living in retirement on his various estates, mainly Blankenburg Castle in Germany and Cumberland Castle in Gmunden, Austria.
He also owned Marienburg Castle near Hanover, although rarely ever living there until 1945.
While Ernest Augustus never officially joined the Nazi Party, he donated funds and was close to several leaders.
As a former British prince, Ernest Augustus, as well as Victoria Louise, desired a rapprochement between the United Kingdom and Germany.
Ostensibly desiring to pursue an alliance with the UK, in the mid-1930s, Adolf Hitler took advantage of their sentiment by asking the couple to arrange a match between their daughter Princess Frederica and the Prince of Wales.
The Duke and Duchess of Brunswick refused, believing that the age difference was too great.
In 1938 Princess Frederica married Prince Paul of Greece, brother and heir-presumptive of King George II of Greece.
Ernest Augustus lived to see his daughter Frederica become a queen consort in 1947 when her husband Paul became King of the Hellenes.
Ernest Augustus died at Marienburg Castle in 1953.
He was interred, later to be joined by the remains of his wife, in front of the Royal Mausoleum in the Berggarten at Herrenhausen Gardens in Hanover, which is the burial chapel of King Ernest Augustus of Hanover and his wife.
Issue

The Duke and Duchess of Brunswick had five children:


Honours

Ancestry

References

Sources

External links



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
  AssignClass (b1878530-7f34-408e-8ba5-50daf74d9f35)
 Call ID: b1878530-7f34-408e-8ba5-50daf74d9f35
  Args:
    source: ErnestAugustus_DukeOfBrunswick
    type: :Man
  AssignClass (9ff69b86-cbc8-4f4a-87ce-ee5a8c9aa218)
 Call ID: 9ff69b86-cbc8-4f4a-87ce-ee5a8c9aa218
  Args:
    source: ErnestAugustus_DukeOfBrunswick
    type: :Person
  AddLiteral (d9eea4a0-f519-4e05-8c73-dc64de324da8)
 Call ID: d9eea4a0-f519-4e05-8c73-dc64de324da8
  Args:
    literal_value: Ernest Augustus Christian George
    relation: :knownAs
    source: ErnestAugustus_DukeOfBrunswick
    literal_type: xsd:string
  AddLiteral (df7e90f8-af2d-46c7-9c74-3f8481458e12)
 Call ID: df7e90f8-af2d-46c7-9c74-3f8481458e12
  Args:
    relation: :hasBirthYear
    literal_value: 1887
    literal_type: xsd:integer
    source: ErnestAugustus_DukeOfBrunswick
  AddLiteral (d3af5e92-a3b5-4182-904c-b56afa0c528e)
 Call ID: d3af5e92-a3b5-4182-904c-b56afa0c528e
  Args:
    source: ErnestAugustus_DukeOfBrunswick
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1953
  AssignClass (f6e25ff9-2797-4ab7-8a55-776bf5eeaf06)
 Call ID: f6e25ff9-2797-4ab7-8a55-776bf5eeaf06
  Args:
    source: ErnestAugustus_CrownPrinceOfHanover
    type: :Man
  AssignClass (e79c0711-9a9b-41cb-ad30-210c896f057b)
 Call ID: e79c0711-9a9b-41cb-ad30-210c896f057b
  Args:
    type: :Person
    source: ErnestAugustus_CrownPrinceOfHanover
  AssignClass (2507bd9c-f251-4f68-a4d9-ea24363a0bcf)
 Call ID: 2507bd9c-f251-4f68-a4d9-ea24363a0bcf
  Args:
    type: :Woman
    source: Thyra_PrincessOfDenmark
  AssignClass (f6778c41-01db-4d80-baae-ef9ba5a143f5)
 Call ID: f6778c41-01db-4d80-baae-ef9ba5a143f5
  Args:
    type: :Person
    source: Thyra_PrincessOfDenmark
  AddTriple (1dd7b969-3333-4260-9e2e-c75387bbb7f3)
 Call ID: 1dd7b969-3333-4260-9e2e-c75387bbb7f3
  Args:
    relation: :hasFather
    target: ErnestAugustus_CrownPrinceOfHanover
    source: ErnestAugustus_DukeOfBrunswick
  AddTriple (ebed034c-ab16-4ac2-a196-cf148f531a11)
 Call ID: ebed034c-ab16-4ac2-a196-cf148f531a11
  Args:
    source: ErnestAugustus_DukeOfBrunswick
    target: Thyra_PrincessOfDenmark
    relation: :hasMother
  AssignClass (5de20e0e-d2ec-496f-a5d8-9a3584089463)
 Call ID: 5de20e0e-d2ec-496f-a5d8-9a3584089463
  Args:
    type: :Man
    source: George_BrotherOfErnestAugustus
  AssignClass (6eff240c-af11-49dd-afeb-a63fd1b10407)
 Call ID: 6eff240c-af11-49dd-afeb-a63fd1b10407
  Args:
    source: George_BrotherOfErnestAugustus
    type: :Person
  AssignClass (76fd78b2-d3ad-45a1-b3a6-7e06f34f4f0b)
 Call ID: 76fd78b2-d3ad-45a1-b3a6-7e06f34f4f0b
  Args:
    type: :Man
    source: Christian_BrotherOfErnestAugustus
  AssignClass (137606b6-9651-4b13-8f34-a81bd8e2fb7d)
 Call ID: 137606b6-9651-4b13-8f34-a81bd8e2fb7d
  Args:
    source: Christian_BrotherOfErnestAugustus
    type: :Person
  AddTriple (9446638f-246d-4809-8665-3cf18cbcfb4d)
 Call ID: 9446638f-246d-4809-8665-3cf18cbcfb4d
  Args:
    relation: :isBrotherOf
    source: George_BrotherOfErnestAugustus
    target: ErnestAugustus_DukeOfBrunswick
  AddTriple (30ef76d8-de10-4a6a-91c3-d4efc88baf74)
 Call ID: 30ef76d8-de10-4a6a-91c3-d4efc88baf74
  Args:
    source: Christian_BrotherOfErnestAugustus
    target: ErnestAugustus_DukeOfBrunswick
    relation: :isBrotherOf
  AssignClass (1529d08d-02c0-41bb-8725-410604c71dc5)
 Call ID: 1529d08d-02c0-41bb-8725-410604c71dc5
  Args:
    type: :Woman
    source: VictoriaLouise_PrincessOfPrussia
  AssignClass (84aa2aac-7d63-457f-b2b8-ab30e3c95444)
 Call ID: 84aa2aac-7d63-457f-b2b8-ab30e3c95444
  Args:
    source: VictoriaLouise_PrincessOfPrussia
    type: :Person
  AddTriple (a23edff1-1468-4500-9865-48774f920025)
 Call ID: a23edff1-1468-4500-9865-48774f920025
  Args:
    target: VictoriaLouise_PrincessOfPrussia
    source: ErnestAugustus_DukeOfBrunswick
    relation: :hasRelation
  AddLiteral (ffefcc16-4b3a-4250-bb23-ed3a8c7ae367)
 Call ID: ffefcc16-4b3a-4250-bb23-ed3a8c7ae367
  Args:
    literal_value: 1913
    relation: :hasMarriageYear
    source: ErnestAugustus_DukeOfBrunswick
    literal_type: xsd:integer
  AssignClass (e956d275-e30c-4aee-a149-63b2dc3f3e63)
 Call ID: e956d275-e30c-4aee-a149-63b2dc3f3e63
  Args:
    type: :Man
    source: ErnestAugustus_SonOfDukeOfBrunswick
  AssignClass (f2bff383-e969-4a9d-b580-a09b3a050a77)
 Call ID: f2bff383-e969-4a9d-b580-a09b3a050a77
  Args:
    type: :Person
    source: ErnestAugustus_SonOfDukeOfBrunswick
  AddTriple (6f17dd37-fd94-45f3-8ba6-989e030350f0)
 Call ID: 6f17dd37-fd94-45f3-8ba6-989e030350f0
  Args:
    relation: :hasFather
    source: ErnestAugustus_SonOfDukeOfBrunswick
    target: ErnestAugustus_DukeOfBrunswick
  AddTriple (3065c4aa-8a18-4b85-b58d-a4321ad6ac38)
 Call ID: 3065c4aa-8a18-4b85-b58d-a4321ad6ac38
  Args:
    relation: :hasMother
    source: ErnestAugustus_SonOfDukeOfBrunswick
    target: VictoriaLouise_PrincessOfPrussia
  AssignClass (60373dec-1d62-4957-9866-a6732e2faafe)
 Call ID: 60373dec-1d62-4957-9866-a6732e2faafe
  Args:
    type: :Woman
    source: Frederica_Princess
  AssignClass (7e88cf48-5cbe-46c1-a2e9-4d76aa1e1d83)
 Call ID: 7e88cf48-5cbe-46c1-a2e9-4d76aa1e1d83
  Args:
    source: Frederica_Princess
    type: :Person
  AddTriple (defb1ec2-b553-4cb7-841e-89a856dd6f0b)
 Call ID: defb1ec2-b553-4cb7-841e-89a856dd6f0b
  Args:
    source: Frederica_Princess
    target: ErnestAugustus_DukeOfBrunswick
    relation: :hasFather
  AddTriple (7515f5b7-5c22-4eaa-897f-79495d3e0f94)
 Call ID: 7515f5b7-5c22-4eaa-897f-79495d3e0f94
  Args:
    relation: :hasMother
    target: VictoriaLouise_PrincessOfPrussia
    source: Frederica_Princess
  AssignClass (28de9ced-06f5-4bc3-9e7e-3b5329bdd309)
 Call ID: 28de9ced-06f5-4bc3-9e7e-3b5329bdd309
  Args:
    type: :Man
    source: Paul_PrinceOfGreece
  AssignClass (9eb7ca30-268f-4e40-990d-f6ddd3f0fb22)
 Call ID: 9eb7ca30-268f-4e40-990d-f6ddd3f0fb22
  Args:
    source: Paul_PrinceOfGreece
    type: :Person
  AddTriple (8490f944-35b1-49df-8b84-706cc72a1f72)
 Call ID: 8490f944-35b1-49df-8b84-706cc72a1f72
  Args:
    relation: :hasRelation
    target: Paul_PrinceOfGreece
    source: Frederica_Princess
  Finish (fcd4be67-92a4-4ec1-a6b1-7b601b8a5cd7)
 Call ID: fcd4be67-92a4-4ec1-a6b1-7b601b8a5cd7
  Args: