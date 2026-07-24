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
Alfonso, Duke of Anjou, Duke of Cádiz, Grandee of Spain (Spanish: Don Alfonso Jaime Marcelino Manuel Víctor María de Borbón y Dampierre; French: Alphonse Jacques Marcellin Emmanuel Victor Marie de Bourbon; 20 April 1936 – 30 January 1989) was a grandson of King Alfonso XIII of Spain, a potential heir to the throne in the event of the restoration of the Spanish monarchy, and the Legitimist claimant to the throne of France.
Upbringing

Alfonso was born at Sant'Anna Clinic in Rome, the elder son of Infante Jaime, Duke of Segovia, King Alfonso's second of four sons.
His mother was Donna Emanuela de Dampierre, daughter of Roger, Duke of San Lorenzo and Donna Vittoria Ruspoli
The Segovias lived in Rome where Jaime's father had maintained a royal court-in-exile since the royal family fled Spain following the 1931 election of republicans and socialists in Spain's major cities.
Alfonso was baptised by Eugenio Cardinal Pacelli (later Pope Pius XII) at the Palazzo Ruspoli on the Via del Corso in Rome, home of his maternal grandmother, Donna Vittoria Ruspoli dei principi di Poggio Suasa.
In 1941, Alfonso and his parents followed his English-born grandmother, Queen Victoria Eugenie to Lausanne in Switzerland.
They lived first at the Hotel Royal, before Alfonso and his younger brother Gonzalo were sent to the Collège Saint-Jean (later Villa St. Jean International School) in Fribourg.
On 8 December 1946 Alfonso made his first communion with his brother, Gonzalo; on the same day he was confirmed by Pedro Cardinal Segura y Sáenz, Archbishop of Seville.
Spanish succession rights

The king's eldest son, Alfonso, Prince of Asturias, had inherited hemophilia from his maternal great-grandmother Queen Victoria, yet had been considered Spain's heir apparent until the republic was established in 1931.
Next in the line of succession, Infante Don Jaime, deaf and largely mute, was that same day persuaded to renounce his claim (and that of future descendants) alongside his elder brother, thereby assuming the Duke of Segovia title and clearing the way for King Alfonso's third son, Don Juan, Count of Barcelona to take up the monarchist cause on behalf of the banished dynasty.
There being no need for Segovia to contract a dynastic alliance, Emanuela de Dampierre's noble rather than royal background was looked upon approvingly by the former king and former queen when the couple wed in Rome in 1935, and neither style nor title is attributed to Alfonso de Borbón-Segovia y Dampierre in the 1944 edition of the Almanach de Gotha.
Following Alfonso XIII's death in Rome in February 1941, Franco wrote Don Juan, acknowledging him as rightful heir to the throne (though without inviting him to occupy it), implicitly confirming that he considered Segovia and his sons excluded from the royal succession.
The new law allowed Franco or his successor to choose any man "of royal lineage" as king, and Alfonso was mentioned that year as a possible alternative to Don Juan and his son, Juan Carlos, should Franco consider the former too liberal to reign over a Falangist Spain.
In December 1949, Segovia retracted his renunciation as coerced and claimed that he was the rightful claimant to Spain's crown.
Relations between Don Juan and Franco continued to deteriorate and in 1952 the latter prevailed upon Segovia to send his elder son to Spain to be educated under his guidance.
Reluctantly, Alfonso moved from Switzerland to Spain, initially to study law at Deusto University and, in 1955 to attend the elite Centro de Estudios Universitarios (CEU).
By 1956 Franco was diverting sponsors of some civic events from Juan Carlos, who was also being educated in Spain under the Caudillo's supervision, to Alfonso.
By 1964, Franco considered Juan Carlos his preferred candidate for the throne over his father, but also considered that if the latter deviated from obedience to Franco or loyalty to his Movimiento Nacional, Alfonso was a suitable alternative.
Alfonso's strongest supporter in Franco's government was José Solís Ruiz, minister and secretary-general of the Movimiento.
Anticipating that Franco would soon offer to declare him Spain's next king rather than Don Juan, in June 1969, Juan Carlos warned his father that if he declined Franco's offer, Alfonso would be invited to accept the crown, nevertheless Don Juan refused to consent to being bypassed.
Asked by Juan Carlos to be chief witness at the ceremony declaring him successor and Prince of Spain, Alfonso immediately agreed to do so and sent some of his supporters to visit his father in Paris to persuade him to express no opposition publicly.
In return for his full support, Franco later appointed Alfonso Spain's ambassador to Sweden.
But in June 1972, after he had taken up that post, Alfonso advised Franco's foreign minister Laureano López Rodó that he deemed his support conditional upon his cousin's continued loyalty to Francoist Spain.
He further hinted that Spain's law of succession should be amended to facilitate Alfonso's replacing or succeeding Juan Carlos as Franco's heir or on the throne, if circumstances called for such a change.
On 8 March 1972, in the Palace of El Pardo in Madrid, Alfonso married Doña María del Carmen Martínez-Bordiú y Franco, daughter of Don Cristóbal Martínez-Bordiú, 10th Marquis de Villaverde, and of his wife, Doña Carmen Franco y Polo (Franco's only daughter.
Doña Carmen was granted a title in 1975 becoming the 1st Duchess de Franco after Franco's death).
The witnesses of the marriage were Franco and Alfonso's mother.
Alfonso and Carmen separated in 1979, received a civil divorce in 1982 and an ecclesiastical annulment in 1986.
On 22 November 1972, General Franco awarded Alfonso the Spanish title Duque de Cádiz with the dignity Grandee of Spain, and he received the style of Royal Highness.
The Cádiz title had been held by Alfonso's great-great-grandfather, the Infante Francisco de Asís.
French succession rights

Since Alfonso's mother was not born a princess of royal descent, his grandfather Alfonso XIII did not consider young Alfonso in line to the Spanish throne in accordance with the Pragmatic Sanction of 1830.
Alfonso's father Jaime, however, came to assert that his sons were French dynasts entitled to the style of Royal Highness.
In Spain up until 1972, Alfonso was generally addressed as Don Alfonso de Borbón y Dampierre.
Elsewhere he was often addressed as a prince.
On 25 November 1950, Alfonso received the title Duc de Bourbon (Duke of Bourbon) from his father.
In 1963, Alfonso engaged the French historian and ardent royalist Hervé Pinoteau as his private secretary.
Pinoteau remained with him until the duke's death.
On 20 March 1975, Alfonso's father Jaime died.
On 3 August 1975, he took the courtesy title Duc d'Anjou (Duke of Anjou).
On 21 January 1985 (the 192nd anniversary of the death of King Louis XVI) Alfonso was present for the requiem mass at the Chapelle expiatoire in Paris.
Marriage and children

Lawsuit of the Count of Clermont against the Duke of Anjou

In 1987, his paternal 10th cousin Prince Henri of Orléans, Count of Clermont, eldest son of Henri, Count of Paris, the then Orléanist claimant to the defunct throne of France, initiated a court action against Alfonso for his use of the title Duke of Anjou and the coat-of-arms France Moderne (three fleur-de-lis or); Henri asked the court to fine Alfonso 50,000 French francs for each future violation.
In 1988, Prince Ferdinand, Duke of Castro and Prince Sixtus Henry of Bourbon-Parma joined Henri's lawsuit in reference to the use of the title Duke of Anjou, but not in respect to the coat-of-arms.
In 1989, Prince Henri d'Orléans and Prince Sixtus Henry of Bourbon-Parma appealed the judgment in the lawsuit about the use of a title and arms by Alfonso; the original judgment in favour of Alfonso was upheld.
Career

From 1977 to 1984, Alfonso was President of the Spanish Skiing Federation, and from 1984 to 1987 President of the Spanish Olympic Committee.
Death

Alfonso died in a skiing accident in Beaver Creek Resort, Eagle County, Colorado, on 30 January 1989, from broken neck by a cable which he collided with as it was being raised to support a banner at the finish line of a course at the FIS Alpine World Ski Championships.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (73e35ebe-9c5d-45f3-9bcc-ddf4bb670a57)
 Call ID: 73e35ebe-9c5d-45f3-9bcc-ddf4bb670a57
  Args:
    source: Alfonso_Duke_of_Anjou
    type: :Man
  AssignClass (e50eddcf-c891-4be0-afcf-1f2e244ffc31)
 Call ID: e50eddcf-c891-4be0-afcf-1f2e244ffc31
  Args:
    type: :Person
    source: Alfonso_Duke_of_Anjou
  AddLiteral (b59fb62b-0262-4771-b2cb-334f21984d9d)
 Call ID: b59fb62b-0262-4771-b2cb-334f21984d9d
  Args:
    literal_value: Alfonso, Duke of Anjou, Duke of Cádiz, Grandee of Spain
    source: Alfonso_Duke_of_Anjou
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (46bd81c7-643c-4479-8928-50567441de25)
 Call ID: 46bd81c7-643c-4479-8928-50567441de25
  Args:
    source: Alfonso_Duke_of_Anjou
    literal_value: 1936
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (066a95bc-efde-44e0-b1ae-279bc1f1093b)
 Call ID: 066a95bc-efde-44e0-b1ae-279bc1f1093b
  Args:
    relation: :hasDeathYear
    literal_value: 1989
    source: Alfonso_Duke_of_Anjou
    literal_type: xsd:integer
  AssignClass (27351a0a-3a28-4333-8256-4a675a121d7c)
 Call ID: 27351a0a-3a28-4333-8256-4a675a121d7c
  Args:
    source: Infante_Jaime_Duke_of_Segovia
    type: :Man
  AssignClass (65883820-00cd-44e7-ac2c-0d7be6d46032)
 Call ID: 65883820-00cd-44e7-ac2c-0d7be6d46032
  Args:
    source: Infante_Jaime_Duke_of_Segovia
    type: :Person
  AddTriple (18a93d9e-e8fe-4fa5-990a-3867457f14af)
 Call ID: 18a93d9e-e8fe-4fa5-990a-3867457f14af
  Args:
    relation: :hasFather
    target: Infante_Jaime_Duke_of_Segovia
    source: Alfonso_Duke_of_Anjou
  AssignClass (5163f4f2-f7be-41b2-90d0-271d3162f7dd)
 Call ID: 5163f4f2-f7be-41b2-90d0-271d3162f7dd
  Args:
    source: Donna_Emanuela_de_Dampierre
    type: :Woman
  AssignClass (b49d0ab6-c921-46a8-b106-e36c80762e2b)
 Call ID: b49d0ab6-c921-46a8-b106-e36c80762e2b
  Args:
    type: :Person
    source: Donna_Emanuela_de_Dampierre
  AddTriple (8b61e150-ed20-4889-95c5-bf69f3be6f36)
 Call ID: 8b61e150-ed20-4889-95c5-bf69f3be6f36
  Args:
    relation: :hasMother
    source: Alfonso_Duke_of_Anjou
    target: Donna_Emanuela_de_Dampierre
  AssignClass (003915eb-1f03-4289-853e-b88f56d0f1ee)
 Call ID: 003915eb-1f03-4289-853e-b88f56d0f1ee
  Args:
    source: Gonzalo
    type: :Man
  AssignClass (d8a4ae3c-96dc-4343-93ec-02290e8b20f1)
 Call ID: d8a4ae3c-96dc-4343-93ec-02290e8b20f1
  Args:
    type: :Person
    source: Gonzalo
  AddTriple (d029268c-661d-43bd-ae9c-5e4da4764d33)
 Call ID: d029268c-661d-43bd-ae9c-5e4da4764d33
  Args:
    target: Alfonso_Duke_of_Anjou
    source: Gonzalo
    relation: :isBrotherOf
  AddTriple (3b1690eb-b2a0-47b3-ac7e-4f344b50a646)
 Call ID: 3b1690eb-b2a0-47b3-ac7e-4f344b50a646
  Args:
    relation: :hasFather
    target: Infante_Jaime_Duke_of_Segovia
    source: Gonzalo
  AddTriple (01cafee5-e9b3-4233-8b19-aca736c93b15)
 Call ID: 01cafee5-e9b3-4233-8b19-aca736c93b15
  Args:
    relation: :hasMother
    target: Donna_Emanuela_de_Dampierre
    source: Gonzalo
  AssignClass (a26bc57a-b007-4b84-ac3a-27304aabc6ae)
 Call ID: a26bc57a-b007-4b84-ac3a-27304aabc6ae
  Args:
    source: King_Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (9dba803d-b0c8-4731-ba4f-660e50d2b8c6)
 Call ID: 9dba803d-b0c8-4731-ba4f-660e50d2b8c6
  Args:
    source: King_Alfonso_XIII_of_Spain
    type: :Person
  AddTriple (657c25f9-8525-4d11-b379-6b551502f42a)
 Call ID: 657c25f9-8525-4d11-b379-6b551502f42a
  Args:
    relation: :isFatherOf
    target: Infante_Jaime_Duke_of_Segovia
    source: King_Alfonso_XIII_of_Spain
  AssignClass (8e341d30-a9fe-4684-b623-cccbfaa53604)
 Call ID: 8e341d30-a9fe-4684-b623-cccbfaa53604
  Args:
    source: Roger_Duke_of_San_Lorenzo
    type: :Man
  AssignClass (779fa9b5-84f0-4208-9584-26addd9b6978)
 Call ID: 779fa9b5-84f0-4208-9584-26addd9b6978
  Args:
    source: Roger_Duke_of_San_Lorenzo
    type: :Person
  AssignClass (3f44054f-ec0e-44e7-97fe-db352ad051fd)
 Call ID: 3f44054f-ec0e-44e7-97fe-db352ad051fd
  Args:
    source: Donna_Vittoria_Ruspoli
    type: :Woman
  AssignClass (981385b0-50be-40cb-8dc2-5751f1b93720)
 Call ID: 981385b0-50be-40cb-8dc2-5751f1b93720
  Args:
    type: :Person
    source: Donna_Vittoria_Ruspoli
  AddTriple (5dfefa36-6d1b-451f-9e66-10d462718165)
 Call ID: 5dfefa36-6d1b-451f-9e66-10d462718165
  Args:
    target: Donna_Emanuela_de_Dampierre
    source: Roger_Duke_of_San_Lorenzo
    relation: :isFatherOf
  AddTriple (9d3c683a-3bbd-4fd9-b961-32aeb0dcc1d5)
 Call ID: 9d3c683a-3bbd-4fd9-b961-32aeb0dcc1d5
  Args:
    relation: :isMotherOf
    target: Donna_Emanuela_de_Dampierre
    source: Donna_Vittoria_Ruspoli
  AssignClass (adeae734-110d-4d50-ba61-172d47d922db)
 Call ID: adeae734-110d-4d50-ba61-172d47d922db
  Args:
    source: Doña_María_del_Carmen_Martínez-Bordiú_y_Franco
    type: :Woman
  AssignClass (3b87c70a-fac9-4e20-b31d-c76f675e2394)
 Call ID: 3b87c70a-fac9-4e20-b31d-c76f675e2394
  Args:
    type: :Person
    source: Doña_María_del_Carmen_Martínez-Bordiú_y_Franco
  AddTriple (ea49a02a-41c3-4078-bb10-b7108c6df7c4)
 Call ID: ea49a02a-41c3-4078-bb10-b7108c6df7c4
  Args:
    target: Doña_María_del_Carmen_Martínez-Bordiú_y_Franco
    source: Alfonso_Duke_of_Anjou
    relation: :hasRelation
  AddLiteral (8875bac8-aa04-42dc-b7f3-664f3b797343)
 Call ID: 8875bac8-aa04-42dc-b7f3-664f3b797343
  Args:
    relation: :hasMarriageYear
    source: Alfonso_Duke_of_Anjou
    literal_value: 1972
    literal_type: xsd:integer
  AssignClass (2c34df3c-4c62-4ae4-bd77-a91b73cb2b68)
 Call ID: 2c34df3c-4c62-4ae4-bd77-a91b73cb2b68
  Args:
    type: :Man
    source: Don_Cristóbal_Martínez-Bordiú
  AssignClass (ea83d2f7-68ec-4f9b-ad69-a5b34f0cfe56)
 Call ID: ea83d2f7-68ec-4f9b-ad69-a5b34f0cfe56
  Args:
    type: :Person
    source: Don_Cristóbal_Martínez-Bordiú
  AssignClass (d16b103f-c59f-42f4-8359-69aa5b2b64e4)
 Call ID: d16b103f-c59f-42f4-8359-69aa5b2b64e4
  Args:
    type: :Woman
    source: Doña_Carmen_Franco_y_Polo
  AssignClass (d9b7d35a-9ee6-485b-99fb-5127f7c1d0e6)
 Call ID: d9b7d35a-9ee6-485b-99fb-5127f7c1d0e6
  Args:
    type: :Person
    source: Doña_Carmen_Franco_y_Polo
  AddTriple (417e6535-f063-4742-b428-429afac18b48)
 Call ID: 417e6535-f063-4742-b428-429afac18b48
  Args:
    relation: :isFatherOf
    source: Don_Cristóbal_Martínez-Bordiú
    target: Doña_María_del_Carmen_Martínez-Bordiú_y_Franco
  AddTriple (bff788c4-d9a1-4bed-b2ef-bcc3ccc2f0b1)
 Call ID: bff788c4-d9a1-4bed-b2ef-bcc3ccc2f0b1
  Args:
    target: Doña_María_del_Carmen_Martínez-Bordiú_y_Franco
    source: Doña_Carmen_Franco_y_Polo
    relation: :isMotherOf
  Finish (e0538e8f-521b-43b2-a53f-c0743d801340)
 Call ID: e0538e8f-521b-43b2-a53f-c0743d801340
  Args: