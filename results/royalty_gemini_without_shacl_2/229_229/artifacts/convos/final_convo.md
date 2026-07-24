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
  AssignClass (ff901da7-5fda-4752-ad15-7ab904182ccf)
 Call ID: ff901da7-5fda-4752-ad15-7ab904182ccf
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    type: :Man
  AssignClass (53b95508-268c-4fe0-b759-b2f286c92071)
 Call ID: 53b95508-268c-4fe0-b759-b2f286c92071
  Args:
    type: :Person
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (19284157-5b19-4646-bf06-f4e1224646c2)
 Call ID: 19284157-5b19-4646-bf06-f4e1224646c2
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Henri_Philippe_Pierre_Marie_dOrleans
    literal_value: 1933
  AddLiteral (9ce730f7-1b64-4e6b-b535-ddf86752cbd1)
 Call ID: 9ce730f7-1b64-4e6b-b535-ddf86752cbd1
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    literal_value: 2019
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (547c23b2-5c1a-4800-bea7-a6119eb50bdd)
 Call ID: 547c23b2-5c1a-4800-bea7-a6119eb50bdd
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (d061d8d0-b93e-4f02-acc0-a5d56b00e418)
 Call ID: d061d8d0-b93e-4f02-acc0-a5d56b00e418
  Args:
    source: Henri_Count_of_Paris
    type: :Person
  AddLiteral (53082534-0cb4-4008-b1df-94af8ec0b633)
 Call ID: 53082534-0cb4-4008-b1df-94af8ec0b633
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1908
    source: Henri_Count_of_Paris
  AddLiteral (8cd2fc56-42d6-465c-9321-d1d36c52fbf9)
 Call ID: 8cd2fc56-42d6-465c-9321-d1d36c52fbf9
  Args:
    literal_value: 1999
    source: Henri_Count_of_Paris
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (886f4120-56d8-455d-90d6-162b78498135)
 Call ID: 886f4120-56d8-455d-90d6-162b78498135
  Args:
    source: Princess_Isabelle_of_Orleans-Braganza
    type: :Woman
  AssignClass (fb4c9312-9600-4b5b-9278-42b3bc5898ce)
 Call ID: fb4c9312-9600-4b5b-9278-42b3bc5898ce
  Args:
    source: Princess_Isabelle_of_Orleans-Braganza
    type: :Person
  AddTriple (9945329f-74bc-4e5e-acf1-4e3562c9172b)
 Call ID: 9945329f-74bc-4e5e-acf1-4e3562c9172b
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
    target: Henri_Count_of_Paris
  AddTriple (c2afc3fb-c81f-4803-b9bd-04ceea44bbee)
 Call ID: c2afc3fb-c81f-4803-b9bd-04ceea44bbee
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Princess_Isabelle_of_Orleans-Braganza
    relation: :hasMother
  AssignClass (a7bda55e-1da9-45ec-8b3e-6fcde3f337fa)
 Call ID: a7bda55e-1da9-45ec-8b3e-6fcde3f337fa
  Args:
    type: :Woman
    source: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (b8c6532f-6545-48bd-a859-64c785d7e777)
 Call ID: b8c6532f-6545-48bd-a859-64c785d7e777
  Args:
    type: :Person
    source: Duchess_Marie_Therese_of_Wurttemberg
  AddLiteral (20c7917f-8f9f-45f1-b2a1-50b27fb64e8f)
 Call ID: 20c7917f-8f9f-45f1-b2a1-50b27fb64e8f
  Args:
    literal_value: 1934
    source: Duchess_Marie_Therese_of_Wurttemberg
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (6f6f601c-cd35-4c0f-9895-92ec416e5d65)
 Call ID: 6f6f601c-cd35-4c0f-9895-92ec416e5d65
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasRelation
    target: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (59da3d0b-a86a-4979-8918-6df6aedd2a46)
 Call ID: 59da3d0b-a86a-4979-8918-6df6aedd2a46
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Woman
  AssignClass (18643e86-94b8-4abf-864d-64fded35cd9a)
 Call ID: 18643e86-94b8-4abf-864d-64fded35cd9a
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Person
  AddLiteral (1aa92d94-7027-49df-93a6-6b6a2e4cf241)
 Call ID: 1aa92d94-7027-49df-93a6-6b6a2e4cf241
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1938
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (a8cd53ef-d3a8-4fd8-866b-09434bd95912)
 Call ID: a8cd53ef-d3a8-4fd8-866b-09434bd95912
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2022
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (35139769-340b-4242-89b0-572070aff137)
 Call ID: 35139769-340b-4242-89b0-572070aff137
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_value: 1984
  AssignClass (ad1e5912-575c-49ad-8631-9ac391495a93)
 Call ID: ad1e5912-575c-49ad-8631-9ac391495a93
  Args:
    source: Luis_Cousino_y_Sebire
    type: :Man
  AssignClass (705d38cf-26d8-4732-926b-f5f5eaa10a66)
 Call ID: 705d38cf-26d8-4732-926b-f5f5eaa10a66
  Args:
    type: :Person
    source: Luis_Cousino_y_Sebire
  AssignClass (2d80a78e-8bb5-48bb-ba5d-2590729f1c0e)
 Call ID: 2d80a78e-8bb5-48bb-ba5d-2590729f1c0e
  Args:
    type: :Woman
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AssignClass (f81c4f41-576f-448c-8c77-54a709183773)
 Call ID: f81c4f41-576f-448c-8c77-54a709183773
  Args:
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Person
  AddTriple (73e7193f-e36a-44e4-ba42-da90b30dc4a9)
 Call ID: 73e7193f-e36a-44e4-ba42-da90b30dc4a9
  Args:
    target: Luis_Cousino_y_Sebire
    relation: :hasFather
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddTriple (43dc014a-9b93-4579-aa27-ead0efd6a534)
 Call ID: 43dc014a-9b93-4579-aa27-ead0efd6a534
  Args:
    target: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    relation: :hasMother
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AssignClass (08c4b775-adb4-41c0-94e8-b4d860a46df5)
 Call ID: 08c4b775-adb4-41c0-94e8-b4d860a46df5
  Args:
    source: Jean-Robert_Boeuf
    type: :Man
  AssignClass (17e78cca-78da-4575-b0ae-14e091ad404a)
 Call ID: 17e78cca-78da-4575-b0ae-14e091ad404a
  Args:
    source: Jean-Robert_Boeuf
    type: :Person
  AssignClass (19727c6d-2134-4b23-b232-f88857ce2404)
 Call ID: 19727c6d-2134-4b23-b232-f88857ce2404
  Args:
    source: Marie_dOrleans
    type: :Woman
  AssignClass (7e0cf2f5-20a4-4a62-ac39-21a94c68ce29)
 Call ID: 7e0cf2f5-20a4-4a62-ac39-21a94c68ce29
  Args:
    source: Marie_dOrleans
    type: :Person
  AddTriple (25c55eb8-2197-45fa-8ae4-d37edfbb4d91)
 Call ID: 25c55eb8-2197-45fa-8ae4-d37edfbb4d91
  Args:
    source: Marie_dOrleans
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
  AddTriple (646471b9-3f6c-4948-90b8-c157b5a5070d)
 Call ID: 646471b9-3f6c-4948-90b8-c157b5a5070d
  Args:
    relation: :hasMother
    target: Duchess_Marie_Therese_of_Wurttemberg
    source: Marie_dOrleans
  AssignClass (7b9ee01b-1b17-455c-a6f4-ed9b4776a04a)
 Call ID: 7b9ee01b-1b17-455c-a6f4-ed9b4776a04a
  Args:
    type: :Man
    source: Prince_Gundakar_of_Liechtenstein
  AssignClass (01538ef1-6644-4724-add0-6f6e0c9f03a9)
 Call ID: 01538ef1-6644-4724-add0-6f6e0c9f03a9
  Args:
    type: :Person
    source: Prince_Gundakar_of_Liechtenstein
  AssignClass (ddbab9e9-5554-47c7-b2ac-d0efdc742606)
 Call ID: ddbab9e9-5554-47c7-b2ac-d0efdc742606
  Args:
    type: :Man
    source: Francois_dOrleans
  AssignClass (b8eb4778-a59d-404d-9519-d19109b57400)
 Call ID: b8eb4778-a59d-404d-9519-d19109b57400
  Args:
    source: Francois_dOrleans
    type: :Person
  AddTriple (38eb0bab-6f4f-4948-ba45-56c00466434b)
 Call ID: 38eb0bab-6f4f-4948-ba45-56c00466434b
  Args:
    source: Francois_dOrleans
    relation: :hasFather
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (274d1ed1-0a01-474e-9907-ec48fe390ef3)
 Call ID: 274d1ed1-0a01-474e-9907-ec48fe390ef3
  Args:
    target: Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasMother
    source: Francois_dOrleans
  AssignClass (2bf529e2-cf03-45f9-8fa3-7c0edd5f1365)
 Call ID: 2bf529e2-cf03-45f9-8fa3-7c0edd5f1365
  Args:
    type: :Woman
    source: Diane_dOrleans
  AssignClass (a5e3b1e1-3461-465a-a0ef-f2140c49850e)
 Call ID: a5e3b1e1-3461-465a-a0ef-f2140c49850e
  Args:
    type: :Person
    source: Diane_dOrleans
  AddTriple (99f16bb4-867d-40e4-8f65-c0e17d119d7d)
 Call ID: 99f16bb4-867d-40e4-8f65-c0e17d119d7d
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Diane_dOrleans
  AddTriple (22b01550-0689-43d4-a672-085d119ed731)
 Call ID: 22b01550-0689-43d4-a672-085d119ed731
  Args:
    source: Diane_dOrleans
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans-Braganza
  AssignClass (4c97172f-50d6-4033-96a6-cd27e394d470)
 Call ID: 4c97172f-50d6-4033-96a6-cd27e394d470
  Args:
    type: :Man
    source: Michel_Count_of_Evreux
  AssignClass (9a00cd72-1b2a-4f8e-bc74-fdc49c45a34e)
 Call ID: 9a00cd72-1b2a-4f8e-bc74-fdc49c45a34e
  Args:
    type: :Person
    source: Michel_Count_of_Evreux
  AddTriple (ccdbce3a-55b4-49a9-9279-48498ef4d0c6)
 Call ID: ccdbce3a-55b4-49a9-9279-48498ef4d0c6
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Michel_Count_of_Evreux
  AddTriple (2503bd78-2208-4a1c-a27a-1be8b1577d4d)
 Call ID: 2503bd78-2208-4a1c-a27a-1be8b1577d4d
  Args:
    source: Michel_Count_of_Evreux
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans-Braganza
  AssignClass (0f4de205-1415-43f0-99dc-78308e02a175)
 Call ID: 0f4de205-1415-43f0-99dc-78308e02a175
  Args:
    source: Thibaut_Count_of_La_Marche
    type: :Man
  AssignClass (a4314aeb-2793-4f07-b385-9d2e0f69f57a)
 Call ID: a4314aeb-2793-4f07-b385-9d2e0f69f57a
  Args:
    source: Thibaut_Count_of_La_Marche
    type: :Person
  AddTriple (64d03db0-9975-4691-b263-de76fe21f099)
 Call ID: 64d03db0-9975-4691-b263-de76fe21f099
  Args:
    source: Thibaut_Count_of_La_Marche
    relation: :hasFather
    target: Henri_Count_of_Paris
  AddTriple (812c0bab-49ea-4353-af69-35eaf6caf796)
 Call ID: 812c0bab-49ea-4353-af69-35eaf6caf796
  Args:
    source: Thibaut_Count_of_La_Marche
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans-Braganza
  AssignClass (524afce0-1397-4528-9e5b-a66e103ef48b)
 Call ID: 524afce0-1397-4528-9e5b-a66e103ef48b
  Args:
    type: :Man
    source: Prince_Jacques_Duke_of_Orleans
  AssignClass (58de42a4-4b57-43b9-bcec-b5b9ee3d73e7)
 Call ID: 58de42a4-4b57-43b9-bcec-b5b9ee3d73e7
  Args:
    source: Prince_Jacques_Duke_of_Orleans
    type: :Person
  AddTriple (6f544fa9-ff4f-42d8-b9c1-9ec9485df547)
 Call ID: 6f544fa9-ff4f-42d8-b9c1-9ec9485df547
  Args:
    source: Prince_Jacques_Duke_of_Orleans
    relation: :hasFather
    target: Henri_Count_of_Paris
  AddTriple (5b3d5f24-d276-4007-96b4-9f65fa6bedef)
 Call ID: 5b3d5f24-d276-4007-96b4-9f65fa6bedef
  Args:
    source: Prince_Jacques_Duke_of_Orleans
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans-Braganza
  AssignClass (f04deb46-d3b1-4690-9d2c-db467b04d9ff)
 Call ID: f04deb46-d3b1-4690-9d2c-db467b04d9ff
  Args:
    type: :Man
    source: Prince_Charles-Louis_dOrleans
  AssignClass (eb66dfec-ed5b-4030-9aff-e1e3e2faa81a)
 Call ID: eb66dfec-ed5b-4030-9aff-e1e3e2faa81a
  Args:
    source: Prince_Charles-Louis_dOrleans
    type: :Person
  AddLiteral (283ca45c-774a-490d-b7bd-1916f973d4df)
 Call ID: 283ca45c-774a-490d-b7bd-1916f973d4df
  Args:
    literal_value: 1972
    source: Prince_Charles-Louis_dOrleans
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (517435ed-07a2-4195-86cf-aa985f798925)
 Call ID: 517435ed-07a2-4195-86cf-aa985f798925
  Args:
    source: Prince_Charles-Louis_dOrleans
    target: Prince_Jacques_Duke_of_Orleans
    relation: :hasFather
  AssignClass (95d05f05-1c45-49ae-a710-74c37bb6a44f)
 Call ID: 95d05f05-1c45-49ae-a710-74c37bb6a44f
  Args:
    source: Prince_Foulques_dOrleans
    type: :Man
  AssignClass (e577d88a-5a91-4683-b5b3-e4a6fd175750)
 Call ID: e577d88a-5a91-4683-b5b3-e4a6fd175750
  Args:
    type: :Person
    source: Prince_Foulques_dOrleans
  AddLiteral (d7afc304-a54e-407f-8d03-58802fa43e6f)
 Call ID: d7afc304-a54e-407f-8d03-58802fa43e6f
  Args:
    source: Prince_Foulques_dOrleans
    literal_value: 1974
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (f8080921-2ec4-47e9-8431-ab0aeb44077c)
 Call ID: f8080921-2ec4-47e9-8431-ab0aeb44077c
  Args:
    source: Prince_Foulques_dOrleans
    target: Prince_Jacques_Duke_of_Orleans
    relation: :hasFather
  AssignClass (ef119eac-549f-473f-afed-a59dd4b340df)
 Call ID: ef119eac-549f-473f-afed-a59dd4b340df
  Args:
    source: Prince_Jean_Duke_of_Vendome
    type: :Man
  AssignClass (5aba19ad-5c83-460f-9955-d16ef1bd1cd6)
 Call ID: 5aba19ad-5c83-460f-9955-d16ef1bd1cd6
  Args:
    source: Prince_Jean_Duke_of_Vendome
    type: :Person
  AddTriple (3763ab05-c7fa-4f16-b2c4-6104f52cdbe7)
 Call ID: 3763ab05-c7fa-4f16-b2c4-6104f52cdbe7
  Args:
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
    source: Prince_Jean_Duke_of_Vendome
  AddTriple (e6bb40e1-ad0d-45c7-b89d-ba95efc09b52)
 Call ID: e6bb40e1-ad0d-45c7-b89d-ba95efc09b52
  Args:
    target: Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasMother
    source: Prince_Jean_Duke_of_Vendome
  AssignClass (72bb0e64-90a2-4a64-92b0-4c758b5f1b56)
 Call ID: 72bb0e64-90a2-4a64-92b0-4c758b5f1b56
  Args:
    source: Louis-Alphonse_Duke_of_Anjou
    type: :Man
  AssignClass (bc4d1b30-040e-4554-bf98-eeee3dd71065)
 Call ID: bc4d1b30-040e-4554-bf98-eeee3dd71065
  Args:
    type: :Person
    source: Louis-Alphonse_Duke_of_Anjou
  Finish (3a9bdcb6-37cf-4b91-a45e-0e9b8024e3ec)
 Call ID: 3a9bdcb6-37cf-4b91-a45e-0e9b8024e3ec
  Args: