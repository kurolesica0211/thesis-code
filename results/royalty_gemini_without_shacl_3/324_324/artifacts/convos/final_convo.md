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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (6c1a5db0-edbd-47cc-94c2-758f140421a9)
 Call ID: 6c1a5db0-edbd-47cc-94c2-758f140421a9
  Args:
    type: :Man
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (8cdda725-48c8-4056-82e1-25a750e6b706)
 Call ID: 8cdda725-48c8-4056-82e1-25a750e6b706
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    literal_value: 1933
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bece6818-8686-489f-b3c9-7c0ad2e962e5)
 Call ID: bece6818-8686-489f-b3c9-7c0ad2e962e5
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasDeathYear
    literal_value: 2019
    literal_type: xsd:integer
  AssignClass (c381fcbb-fa7d-4284-96b4-41650f304cc7)
 Call ID: c381fcbb-fa7d-4284-96b4-41650f304cc7
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AddLiteral (3b2e669f-1b89-4b3f-9438-6a880489cf83)
 Call ID: 3b2e669f-1b89-4b3f-9438-6a880489cf83
  Args:
    source: Henri_Count_of_Paris
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1908
  AddLiteral (2f7ee91a-449e-4400-902d-25956bbb9e7e)
 Call ID: 2f7ee91a-449e-4400-902d-25956bbb9e7e
  Args:
    source: Henri_Count_of_Paris
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1999
  AssignClass (7742cd49-5a9c-4e62-849d-43fdff365ea1)
 Call ID: 7742cd49-5a9c-4e62-849d-43fdff365ea1
  Args:
    type: :Woman
    source: Isabelle_of_Orleans-Braganza
  AddTriple (97819433-da27-4d88-8226-8861be243fdb)
 Call ID: 97819433-da27-4d88-8226-8861be243fdb
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Henri_Count_of_Paris
    relation: :hasFather
  AddTriple (84630d75-7f51-4f99-8e46-7f7e9169e807)
 Call ID: 84630d75-7f51-4f99-8e46-7f7e9169e807
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Isabelle_of_Orleans-Braganza
    relation: :hasMother
  AssignClass (100159c5-1233-4d06-a8d7-0e49ee7be18a)
 Call ID: 100159c5-1233-4d06-a8d7-0e49ee7be18a
  Args:
    type: :Woman
    source: Marie_Therese_of_Wurttemberg
  AddLiteral (140ce315-e5b4-4014-960e-5af1578a5c32)
 Call ID: 140ce315-e5b4-4014-960e-5af1578a5c32
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1934
    source: Marie_Therese_of_Wurttemberg
  AddTriple (f0830091-9580-4b58-800a-f65b2f8f0d79)
 Call ID: f0830091-9580-4b58-800a-f65b2f8f0d79
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasRelation
    target: Marie_Therese_of_Wurttemberg
  AssignClass (c0058463-9019-415d-b7c3-b01b78455429)
 Call ID: c0058463-9019-415d-b7c3-b01b78455429
  Args:
    type: :Woman
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (7aa9321c-b842-4810-90f1-d79978920b80)
 Call ID: 7aa9321c-b842-4810-90f1-d79978920b80
  Args:
    relation: :hasBirthYear
    literal_value: 1938
    literal_type: xsd:integer
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (7a71ceed-35db-41ac-b35b-588a80f3f864)
 Call ID: 7a71ceed-35db-41ac-b35b-588a80f3f864
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_value: 2022
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (f9590d98-386e-4353-b50f-e11625ad8dd6)
 Call ID: f9590d98-386e-4353-b50f-e11625ad8dd6
  Args:
    relation: :hasRelation
    target: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (acbdac28-49e5-4c78-9729-039ece635120)
 Call ID: acbdac28-49e5-4c78-9729-039ece635120
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1984
  AssignClass (0c796211-ffa8-40b7-b8a5-07143005d714)
 Call ID: 0c796211-ffa8-40b7-b8a5-07143005d714
  Args:
    type: :Man
    source: Luis_Cousino_y_Sebire
  AssignClass (68d0cf4f-868a-4b9a-9751-d7f79a6091cc)
 Call ID: 68d0cf4f-868a-4b9a-9751-d7f79a6091cc
  Args:
    type: :Woman
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AddTriple (769e0056-c96d-453d-898f-4a3bfb83c73d)
 Call ID: 769e0056-c96d-453d-898f-4a3bfb83c73d
  Args:
    target: Luis_Cousino_y_Sebire
    relation: :hasFather
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddTriple (cbeb898e-da6f-4c83-84be-c512f27f7465)
 Call ID: cbeb898e-da6f-4c83-84be-c512f27f7465
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    relation: :hasMother
  AssignClass (35718442-72f5-4a15-a0e3-f61783de0e54)
 Call ID: 35718442-72f5-4a15-a0e3-f61783de0e54
  Args:
    type: :Man
    source: Jean-Robert_Boeuf
  AddTriple (0b83321c-2200-4755-bcf7-08ecfc754fd3)
 Call ID: 0b83321c-2200-4755-bcf7-08ecfc754fd3
  Args:
    target: Jean-Robert_Boeuf
    relation: :hasRelation
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AssignClass (7093775d-af6f-4837-9f3c-eb1543df5e9c)
 Call ID: 7093775d-af6f-4837-9f3c-eb1543df5e9c
  Args:
    type: :Woman
    source: Marie_of_Liechtenstein
  AddTriple (adde401b-4533-4836-aa1c-bd4effb739d8)
 Call ID: adde401b-4533-4836-aa1c-bd4effb739d8
  Args:
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
    source: Marie_of_Liechtenstein
  AddTriple (8724addd-c151-48c7-923d-3cf82cb787d3)
 Call ID: 8724addd-c151-48c7-923d-3cf82cb787d3
  Args:
    source: Marie_of_Liechtenstein
    target: Marie_Therese_of_Wurttemberg
    relation: :hasMother
  AssignClass (d7cdf675-55ea-4986-9afa-f9807eb6fd3b)
 Call ID: d7cdf675-55ea-4986-9afa-f9807eb6fd3b
  Args:
    type: :Man
    source: Gundakar_of_Liechtenstein
  AddTriple (748ed64c-049e-4513-ae36-7ba40f13d63d)
 Call ID: 748ed64c-049e-4513-ae36-7ba40f13d63d
  Args:
    relation: :hasRelation
    target: Gundakar_of_Liechtenstein
    source: Marie_of_Liechtenstein
  AssignClass (877207c4-0c59-46b5-b89d-bdbc4a56fbd8)
 Call ID: 877207c4-0c59-46b5-b89d-bdbc4a56fbd8
  Args:
    type: :Man
    source: Francois_dOrleans
  AddTriple (e1820a30-2465-4cfc-b0da-7f0831538406)
 Call ID: e1820a30-2465-4cfc-b0da-7f0831538406
  Args:
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
    source: Francois_dOrleans
  AssignClass (7e907a02-f2ff-4889-b20f-caa8ff70a130)
 Call ID: 7e907a02-f2ff-4889-b20f-caa8ff70a130
  Args:
    type: :Man
    source: Michel_dOrleans
  AddTriple (f9fc9930-1f3d-49fe-a30b-916fec4e8c5c)
 Call ID: f9fc9930-1f3d-49fe-a30b-916fec4e8c5c
  Args:
    relation: :hasBrother
    target: Michel_dOrleans
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (ef5659c0-f957-42b3-9fb6-80e7f74685ef)
 Call ID: ef5659c0-f957-42b3-9fb6-80e7f74685ef
  Args:
    type: :Man
    source: Thibaut_dOrleans
  AddTriple (5f260ce6-b5ec-4221-9410-25b6a0709164)
 Call ID: 5f260ce6-b5ec-4221-9410-25b6a0709164
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Thibaut_dOrleans
    relation: :hasBrother
  AssignClass (4af46a82-fcba-45b6-b166-471fccaa37db)
 Call ID: 4af46a82-fcba-45b6-b166-471fccaa37db
  Args:
    type: :Man
    source: Jacques_dOrleans
  AddTriple (ec1386b4-08aa-4f95-90db-974f796f48d6)
 Call ID: ec1386b4-08aa-4f95-90db-974f796f48d6
  Args:
    relation: :hasBrother
    target: Jacques_dOrleans
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (45972113-f31d-421b-b18d-e34119243d9c)
 Call ID: 45972113-f31d-421b-b18d-e34119243d9c
  Args:
    type: :Man
    source: Charles-Louis_dOrleans
  AddLiteral (80e134a6-12da-46e4-8f5d-d666654705e2)
 Call ID: 80e134a6-12da-46e4-8f5d-d666654705e2
  Args:
    source: Charles-Louis_dOrleans
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1972
  AddTriple (cd067a3c-ab8f-473d-a9f4-0c55a2232258)
 Call ID: cd067a3c-ab8f-473d-a9f4-0c55a2232258
  Args:
    relation: :hasFather
    target: Jacques_dOrleans
    source: Charles-Louis_dOrleans
  AssignClass (85036592-4a34-40af-8397-f05574f99fad)
 Call ID: 85036592-4a34-40af-8397-f05574f99fad
  Args:
    type: :Man
    source: Foulques_dOrleans
  AddLiteral (7ec713d0-a9cc-4f64-8cf9-8e6ebf3c75d8)
 Call ID: 7ec713d0-a9cc-4f64-8cf9-8e6ebf3c75d8
  Args:
    relation: :hasBirthYear
    literal_value: 1974
    literal_type: xsd:integer
    source: Foulques_dOrleans
  AddTriple (6ec4f1dc-6b43-4732-b135-99ce9c85369b)
 Call ID: 6ec4f1dc-6b43-4732-b135-99ce9c85369b
  Args:
    target: Jacques_dOrleans
    relation: :hasFather
    source: Foulques_dOrleans
  AssignClass (a587caee-2497-4a4f-aa27-121bf6ef218d)
 Call ID: a587caee-2497-4a4f-aa27-121bf6ef218d
  Args:
    type: :Woman
    source: Diane_dOrleans
  AddTriple (9b3d3815-e272-4e8f-a1f1-1fb41074b8b1)
 Call ID: 9b3d3815-e272-4e8f-a1f1-1fb41074b8b1
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasSister
    target: Diane_dOrleans
  AssignClass (340e5800-5e41-469c-9351-9d176b288ce9)
 Call ID: 340e5800-5e41-469c-9351-9d176b288ce9
  Args:
    type: :Man
    source: Jean_dOrleans
  AddTriple (d69f70c4-0761-4302-a951-8471670962eb)
 Call ID: d69f70c4-0761-4302-a951-8471670962eb
  Args:
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
    source: Jean_dOrleans
  Finish (db83a51d-bc01-4cfc-b69a-282639f0141e)
 Call ID: db83a51d-bc01-4cfc-b69a-282639f0141e
  Args: