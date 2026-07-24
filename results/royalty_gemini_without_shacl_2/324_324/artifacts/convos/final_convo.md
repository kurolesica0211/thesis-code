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
  AssignClass (130e088e-fb4e-4f86-a314-5b9cbd641897)
 Call ID: 130e088e-fb4e-4f86-a314-5b9cbd641897
  Args:
    type: :Man
    source: :Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (66f07129-0cc2-4420-8330-36b165c41aea)
 Call ID: 66f07129-0cc2-4420-8330-36b165c41aea
  Args:
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1933
  AddLiteral (7b9ca7cc-3408-464e-ad64-a78df24c65fd)
 Call ID: 7b9ca7cc-3408-464e-ad64-a78df24c65fd
  Args:
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2019
  AssignClass (92cfc9b0-51c3-4897-95f5-4bbf4a52d459)
 Call ID: 92cfc9b0-51c3-4897-95f5-4bbf4a52d459
  Args:
    source: :Henri_Count_of_Paris
    type: :Man
  AddLiteral (e353fa99-5bd2-4009-a815-1ef01fbcaa62)
 Call ID: e353fa99-5bd2-4009-a815-1ef01fbcaa62
  Args:
    source: :Henri_Count_of_Paris
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1908
  AddLiteral (bc32a8e1-3b52-4b8f-8b53-727077d7199c)
 Call ID: bc32a8e1-3b52-4b8f-8b53-727077d7199c
  Args:
    source: :Henri_Count_of_Paris
    literal_type: xsd:integer
    literal_value: 1999
    relation: :hasDeathYear
  AssignClass (b71dc99f-fec9-4ba7-88d4-b9e3fbb178a9)
 Call ID: b71dc99f-fec9-4ba7-88d4-b9e3fbb178a9
  Args:
    source: :Princess_Isabelle_of_Orleans-Braganza
    type: :Woman
  AddTriple (78a8b2da-1825-492d-9a3d-df9212d2999a)
 Call ID: 78a8b2da-1825-492d-9a3d-df9212d2999a
  Args:
    target: :Henri_Count_of_Paris
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
  AddTriple (c564fb1a-ee52-473e-a066-c96f1b1157c1)
 Call ID: c564fb1a-ee52-473e-a066-c96f1b1157c1
  Args:
    relation: :hasMother
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Princess_Isabelle_of_Orleans-Braganza
  AssignClass (321af648-9cb3-4ed3-b673-89803f284624)
 Call ID: 321af648-9cb3-4ed3-b673-89803f284624
  Args:
    source: :Marie_Therese_of_Wurttemberg
    type: :Woman
  AddLiteral (a151d794-ef30-444b-a9f8-eae8676ba111)
 Call ID: a151d794-ef30-444b-a9f8-eae8676ba111
  Args:
    literal_type: xsd:integer
    source: :Marie_Therese_of_Wurttemberg
    literal_value: 1934
    relation: :hasBirthYear
  AssignClass (bb2da0e4-d724-4fd5-b7c5-3d1b4128dcfc)
 Call ID: bb2da0e4-d724-4fd5-b7c5-3d1b4128dcfc
  Args:
    type: :Woman
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (90580138-8e6d-49ab-96fc-6efb6bc9ebde)
 Call ID: 90580138-8e6d-49ab-96fc-6efb6bc9ebde
  Args:
    relation: :hasBirthYear
    literal_value: 1938
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
  AddLiteral (d2ed88f4-388d-4751-824c-0527daf5159e)
 Call ID: d2ed88f4-388d-4751-824c-0527daf5159e
  Args:
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
    literal_value: 2022
    relation: :hasDeathYear
  AddLiteral (8c82a88c-30ba-4d39-abbb-85958fbaef33)
 Call ID: 8c82a88c-30ba-4d39-abbb-85958fbaef33
  Args:
    literal_type: xsd:integer
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasMarriageYear
    literal_value: 1984
  AssignClass (67860ea1-402a-4a78-92d6-e28934f77f89)
 Call ID: 67860ea1-402a-4a78-92d6-e28934f77f89
  Args:
    source: :Luis_Cousino_y_Sebire
    type: :Man
  AssignClass (8335f68b-a6ed-47fc-a030-891a1d18feed)
 Call ID: 8335f68b-a6ed-47fc-a030-891a1d18feed
  Args:
    source: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Woman
  AddTriple (c12e5251-43c3-42c7-93a2-63cc3d398800)
 Call ID: c12e5251-43c3-42c7-93a2-63cc3d398800
  Args:
    relation: :hasFather
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: :Luis_Cousino_y_Sebire
  AddTriple (3a48cb51-0ab8-42fe-bdc9-c7fa1f2e6f40)
 Call ID: 3a48cb51-0ab8-42fe-bdc9-c7fa1f2e6f40
  Args:
    relation: :hasMother
    target: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AssignClass (1d5c0d14-4077-478f-ae16-653287ba98b2)
 Call ID: 1d5c0d14-4077-478f-ae16-653287ba98b2
  Args:
    type: :Man
    source: :Jean-Robert_Boeuf
  AssignClass (3489bd04-21cb-4b69-90fd-e0982c8faaa3)
 Call ID: 3489bd04-21cb-4b69-90fd-e0982c8faaa3
  Args:
    type: :Woman
    source: :Marie_de_Liechtenstein
  AddTriple (c9dd247b-36a8-4888-9268-8c23c0dc45f1)
 Call ID: c9dd247b-36a8-4888-9268-8c23c0dc45f1
  Args:
    relation: :hasFather
    source: :Marie_de_Liechtenstein
    target: :Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (8e300408-1e31-4d7f-a0bd-24d5fcf3f103)
 Call ID: 8e300408-1e31-4d7f-a0bd-24d5fcf3f103
  Args:
    relation: :hasMother
    target: :Marie_Therese_of_Wurttemberg
    source: :Marie_de_Liechtenstein
  AssignClass (20246dc8-7770-42a0-8c6c-8e05d4475114)
 Call ID: 20246dc8-7770-42a0-8c6c-8e05d4475114
  Args:
    source: :Prince_Gundakar_of_Liechtenstein
    type: :Man
  AssignClass (c838620e-d9d4-4bac-9971-f81efb89eee6)
 Call ID: c838620e-d9d4-4bac-9971-f81efb89eee6
  Args:
    type: :Woman
    source: :Diane_of_Orleans
  AddTriple (1e782a50-3bc3-4732-ab69-e65269c5141b)
 Call ID: 1e782a50-3bc3-4732-ab69-e65269c5141b
  Args:
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Diane_of_Orleans
    relation: :hasSister
  AssignClass (ccf56345-e56f-4eb0-b84c-fa3039cf95ee)
 Call ID: ccf56345-e56f-4eb0-b84c-fa3039cf95ee
  Args:
    type: :Man
    source: :Michel_Count_of_Evreux
  AddTriple (6633ae4a-8c19-41e2-a017-63499b34ec1f)
 Call ID: 6633ae4a-8c19-41e2-a017-63499b34ec1f
  Args:
    relation: :hasBrother
    target: :Michel_Count_of_Evreux
    source: :Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (7c6e1403-e497-4d57-8c91-0ddd204401a6)
 Call ID: 7c6e1403-e497-4d57-8c91-0ddd204401a6
  Args:
    type: :Man
    source: :Thibaut_Count_of_La_Marche
  AddTriple (284c8abc-976b-4fec-8b76-2ac847132a80)
 Call ID: 284c8abc-976b-4fec-8b76-2ac847132a80
  Args:
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Thibaut_Count_of_La_Marche
    relation: :hasBrother
  AssignClass (a0624a7f-3fa5-4261-a91a-33c2d0103100)
 Call ID: a0624a7f-3fa5-4261-a91a-33c2d0103100
  Args:
    source: :Jacques_Duke_of_Orleans
    type: :Man
  AddTriple (fbe8a17c-9749-4739-91a0-f5e56e0e8baa)
 Call ID: fbe8a17c-9749-4739-91a0-f5e56e0e8baa
  Args:
    target: :Jacques_Duke_of_Orleans
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasBrother
  AssignClass (dcba8568-ce9c-43c7-8c86-bdb795426302)
 Call ID: dcba8568-ce9c-43c7-8c86-bdb795426302
  Args:
    source: :Charles-Louis_dOrleans_Duke_of_Chartres
    type: :Man
  AddLiteral (27598c78-10ba-412f-9df8-3b12edb0b01e)
 Call ID: 27598c78-10ba-412f-9df8-3b12edb0b01e
  Args:
    source: :Charles-Louis_dOrleans_Duke_of_Chartres
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1972
  AddTriple (c00333d0-c80b-44a1-9dd0-02e7929f5272)
 Call ID: c00333d0-c80b-44a1-9dd0-02e7929f5272
  Args:
    relation: :hasFather
    source: :Charles-Louis_dOrleans_Duke_of_Chartres
    target: :Jacques_Duke_of_Orleans
  AssignClass (089b1da2-dcd6-49e9-bdcf-0af1a752b94c)
 Call ID: 089b1da2-dcd6-49e9-bdcf-0af1a752b94c
  Args:
    type: :Man
    source: :Foulques_dOrleans_Duke_of_Aumale_and_Count_of_Eu
  AddLiteral (a863ceda-5871-4df2-aed8-25c3d8fd533d)
 Call ID: a863ceda-5871-4df2-aed8-25c3d8fd533d
  Args:
    literal_type: xsd:integer
    source: :Foulques_dOrleans_Duke_of_Aumale_and_Count_of_Eu
    relation: :hasBirthYear
    literal_value: 1974
  AddTriple (7c782699-1aac-413d-bed9-4a5e91fbd812)
 Call ID: 7c782699-1aac-413d-bed9-4a5e91fbd812
  Args:
    relation: :hasFather
    target: :Jacques_Duke_of_Orleans
    source: :Foulques_dOrleans_Duke_of_Aumale_and_Count_of_Eu
  AssignClass (6c6c536d-c029-44c4-8517-ff182270cff0)
 Call ID: 6c6c536d-c029-44c4-8517-ff182270cff0
  Args:
    type: :Man
    source: :Francois_Count_of_Clermont
  AddTriple (e095172f-ecfd-4ad9-ac3d-5818630acf44)
 Call ID: e095172f-ecfd-4ad9-ac3d-5818630acf44
  Args:
    target: :Henri_Philippe_Pierre_Marie_dOrleans
    source: :Francois_Count_of_Clermont
    relation: :hasFather
  AddTriple (16cae720-605e-466b-a0a6-4e70c407bc69)
 Call ID: 16cae720-605e-466b-a0a6-4e70c407bc69
  Args:
    relation: :hasMother
    source: :Francois_Count_of_Clermont
    target: :Marie_Therese_of_Wurttemberg
  AssignClass (dac956d7-f34d-4b16-9b91-0804fdba0a78)
 Call ID: dac956d7-f34d-4b16-9b91-0804fdba0a78
  Args:
    type: :Man
    source: :Jean_Duke_of_Vendome
  AddTriple (993fdc08-1ffd-4794-90e0-5d753fe18782)
 Call ID: 993fdc08-1ffd-4794-90e0-5d753fe18782
  Args:
    source: :Jean_Duke_of_Vendome
    target: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
  AddTriple (5e5e3394-d1ef-435e-9db1-7cd96d794119)
 Call ID: 5e5e3394-d1ef-435e-9db1-7cd96d794119
  Args:
    relation: :hasMother
    target: :Marie_Therese_of_Wurttemberg
    source: :Jean_Duke_of_Vendome
  Finish (9e1963f2-0fda-428c-8b50-7af00f81daef)
 Call ID: 9e1963f2-0fda-428c-8b50-7af00f81daef
  Args: